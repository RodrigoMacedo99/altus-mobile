import os
import json
import asyncio
from typing import Dict, Any, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pycomm3 import LogixDriver
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GatewaySockets")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

IS_MOCK = os.getenv("MOCK_PLC", "true").lower() == "true"
CLP_IP = os.getenv("CLP_IP", "192.168.0.100")
SLOT = int(os.getenv("CLP_SLOT", "0"))

# TAG MAPPER 
# ATENÇÃO: EtherNet/IP (pycomm3) utiliza Nomes de Tags (simbólicos) criados no MasterTool, ex: 'GVL_Kit1.Botao1'.
# Endereços diretos como '%IX0.0' costumam falhar com EtherNet/IP. 
# Se o PLC rejeitar as leituras, altere '%IX0.0:BOOL' pelo nome simbólico correto do tag.
TAG_MAP = {
    "altus/kit1/pushbutton/1": "%IX0.0:BOOL",
    "altus/kit1/pushbutton/2": "%IX0.1:BOOL",
    "altus/kit1/pushbutton/3": "%IX0.2:BOOL",
    "altus/kit1/pushbutton/4": "%IX0.3:BOOL",
    
    "altus/kit1/switch/1": "%IX0.4:BOOL",
    "altus/kit1/switch/2": "%IX0.5:BOOL",
    "altus/kit1/switch/3": "%IX0.6:BOOL",
    "altus/kit1/switch/4": "%IX0.7:BOOL",
    
    "altus/kit1/led/1": "%QX0.0:BOOL",
    "altus/kit1/led/2": "%QX0.1:BOOL",
    "altus/kit1/led/3": "%QX0.2:BOOL",
    "altus/kit1/led/4": "%QX0.3:BOOL",
    "altus/kit1/led/5": "%QX0.4:BOOL",
    "altus/kit1/led/6": "%QX0.5:BOOL",
    "altus/kit1/led/7": "%QX0.6:BOOL",
    "altus/kit1/led/8": "%QX0.7:BOOL",
}

class PlcConnection:
    def __init__(self):
        self.plc = None
        self.mock_values = {}
        if not IS_MOCK:
            self.connect()
            
    def connect(self):
        try:
            self.plc = LogixDriver(CLP_IP)
            self.plc.open()
            logger.info(f"Connected to PLC successfully at {CLP_IP}")
        except Exception as e:
            logger.error(f"Failed to connect to PLC: {e}")
            self.plc = None

    def write_tag(self, mobile_tag: str, value: str):
        if "kit2" in mobile_tag:
            return
            
        plc_tag = TAG_MAP.get(mobile_tag)
        if not plc_tag:
            logger.warning(f"Ignoring write for unknown tag: {mobile_tag}")
            return
            
        if IS_MOCK:
            logger.info(f"[MOCK] Writing to {plc_tag} ({mobile_tag}) value: {value}")
            self.mock_values[mobile_tag] = value
            return
            
        if not self.plc or not self.plc.connected:
            self.connect()
            
        if self.plc and self.plc.connected:
            try:
                boolean_value = (value == "1" or str(value).lower() == "true")
                self.plc.write((plc_tag, boolean_value))
                logger.info(f"Wrote to PLC: {plc_tag} = {boolean_value}")
            except Exception as e:
                logger.error(f"Failed to write to PLC tag {plc_tag}: {e}")

    def poll_tags(self) -> Dict[str, str]:
        results = {}
        tags_to_poll = list(TAG_MAP.keys())
        
        if IS_MOCK:
            for tag in tags_to_poll:
                results[tag] = self.mock_values.get(tag, "0")
            return results
            
        if not self.plc or not self.plc.connected:
            self.connect()
            
        if self.plc and self.plc.connected:
            try:
                plc_tags_to_read = [TAG_MAP[mtag] for mtag in tags_to_poll]
                reads = self.plc.read(*plc_tags_to_read)
                
                if not isinstance(reads, list):
                    reads = [reads]
                    
                for i, mobile_tag in enumerate(tags_to_poll):
                    res = reads[i]
                    if res and res.error is None:
                        results[mobile_tag] = "1" if res.value else "0"
            except Exception as e:
                logger.error(f"Failed to read from PLC: {e}")
                
        return results

plc_conn = PlcConnection()
connected_clients: List[WebSocket] = []

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(polling_task())

async def polling_task():
    last_states = {}
    while True:
        try:
            current_states = plc_conn.poll_tags()
            changed_states = {
                tag: val for tag, val in current_states.items() 
                if last_states.get(tag) != val
            }
            
            if changed_states:
                last_states = current_states
                for tag, value in changed_states.items():
                    update = {"action": "update", "tag": tag, "value": value}
                    json_update = json.dumps(update)
                    
                    # Notificar clients em paralelo para evitar bloqueios
                    disconnected = []
                    for client in connected_clients:
                        try:
                            await client.send_text(json_update)
                        except Exception as e:
                            logger.error(f"Failed to send update: {e}")
                            disconnected.append(client)
                            
                    for client in disconnected:
                        if client in connected_clients:
                            connected_clients.remove(client)
                            
        except Exception as e:
            logger.error(f"Error during PLC polling: {e}")
            
        await asyncio.sleep(0.2)

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    client_id = id(websocket)
    logger.info(f"Client connected: ID {client_id}")
    
    try:
        while True:
            text = await websocket.receive_text()
            logger.info(f"Received from ID {client_id}: {text}")
            
            try:
                command = json.loads(text)
                if command.get("action") == "write":
                    plc_conn.write_tag(command.get("tag", ""), command.get("value", ""))
            except Exception as e:
                logger.error(f"Failed to parse incoming command: {text}. Error: {e}")
    except WebSocketDisconnect:
        logger.info(f"Client disconnected: ID {client_id}")
    except Exception as e:
        logger.error(f"Error in websocket session ID {client_id}: {e}")
    finally:
        if websocket in connected_clients:
            connected_clients.remove(websocket)
