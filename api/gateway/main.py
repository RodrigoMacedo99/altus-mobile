import os
import json
import asyncio
from typing import Dict, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pycomm3 import CIPDriver  # Usando o modo CIP puro, não Logix!
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
CLP_IP = os.getenv("CLP_IP", "192.168.15.1")

# ==============================================================================
# MAPEAMENTO DE BITS (Baseado no Assembly EtherNet/IP do MasterTool)
# ==============================================================================

# Entradas (Botões e Switches) - Serão lidas da Instância 101 (Input Assembly)
INPUT_BITS = {
    "altus/kit1/pushbutton/1": 0,  # Bit 0
    "altus/kit1/pushbutton/2": 1,  # Bit 1
    "altus/kit1/pushbutton/3": 2,  # Bit 2
    "altus/kit1/pushbutton/4": 3,  # Bit 3
    "altus/kit1/switch/1": 4,      # Bit 4
    "altus/kit1/switch/2": 5,      # Bit 5
    "altus/kit1/switch/3": 6,      # Bit 6
    "altus/kit1/switch/4": 7,      # Bit 7
}

# Saídas (LEDs) - Serão escritas na Instância 100 (Output Assembly)
OUTPUT_BITS = {
    "altus/kit1/led/1": 0,  # Bit 0
    "altus/kit1/led/2": 1,  # Bit 1
    "altus/kit1/led/3": 2,  # Bit 2
    "altus/kit1/led/4": 3,  # Bit 3
    "altus/kit1/led/5": 4,  # Bit 4
    "altus/kit1/led/6": 5,  # Bit 5
    "altus/kit1/led/7": 6,  # Bit 6
    "altus/kit1/led/8": 7,  # Bit 7
}

class PlcConnection:
    def __init__(self):
        self.mock_values = {}
        self.current_output_byte = 0  # Mantém estado dos LEDs
        self.plc = None
        
        # Inicia a conexão uma única vez ao criar a classe
        if not IS_MOCK:
            try:
                self.plc = CIPDriver(CLP_IP)
                self.plc.open()
                logger.info(f"Conexão persistente estabelecida com o CLP {CLP_IP}")
            except Exception as e:
                logger.error(f"Falha ao conectar no CLP na inicialização: {e}")

    def write_tag(self, mobile_tag: str, value: str):
        if "kit2" in mobile_tag:
            logger.warning(f"Ignorando escrita: tag {mobile_tag} pertence ao kit2.")
            return

        # Mapeamento para permitir que botões e switches do celular controlem os LEDs diretamente.
        if "pushbutton" in mobile_tag:
            mobile_tag = mobile_tag.replace("pushbutton", "led")
        elif "switch" in mobile_tag:
            parts = mobile_tag.split("/")
            if len(parts) == 4:
                idx = int(parts[3])
                # Switches 1-4 são mapeados para os LEDs 5-8
                mobile_tag = f"{parts[0]}/{parts[1]}/led/{idx + 4}"
            
        if IS_MOCK:
            logger.info(f"[MOCK] Writing to {mobile_tag} value: {value}")
            self.mock_values[mobile_tag] = value
            return
            
        if mobile_tag not in OUTPUT_BITS:
            logger.warning(f"Ignorando escrita: tag {mobile_tag} não está configurada em OUTPUT_BITS.")
            return
            
        if self.plc is None:
            logger.error("CLP não conectado. Ignorando escrita.")
            return
            
        try:
            bit_index = OUTPUT_BITS[mobile_tag]
            is_on = (str(value) == "1" or str(value).lower() == "true")
            
            if is_on:
                self.current_output_byte |= (1 << bit_index)
            else:
                self.current_output_byte &= ~(1 << bit_index)
            
            dados_bytes = self.current_output_byte.to_bytes(1, byteorder='little')
            
            # Usamos self.plc diretamente, sem o bloco 'with'
            response = self.plc.generic_message(
                service=0x10,
                class_code=0x04,
                instance=100,
                attribute=0x03,
                request_data=dados_bytes
            )
            
            if response and not response.error:
                logger.info(f"Escrita OK: {mobile_tag} -> Byte enviado: {self.current_output_byte}")
            else:
                logger.error(f"Erro do CLP na escrita: {response.error}")
                
        except Exception as e:
            logger.error(f"Falha ao escrever no Altus: {e}")

    def poll_tags(self) -> Dict[str, str]:
        results = {}
        
        if IS_MOCK:
            for tag in list(INPUT_BITS.keys()) + list(OUTPUT_BITS.keys()):
                results[tag] = self.mock_values.get(tag, "0")
            return results
            
        if self.plc is None:
            # Retorna tudo zero se não houver conexão
            for tag in list(INPUT_BITS.keys()) + list(OUTPUT_BITS.keys()):
                results[tag] = "0"
            return results
            
        try:
            # Usamos self.plc diretamente, sem o bloco 'with'
            response = self.plc.generic_message(
                service=0x0E,
                class_code=0x04,
                instance=101,
                attribute=0x03
            )
            
            if response and not response.error:
                byte_lido = response.value[0]
                for tag, bit_index in INPUT_BITS.items():
                    results[tag] = "1" if (byte_lido & (1 << bit_index)) else "0"
            else:
                logger.error(f"Erro do CLP na leitura: {response.error}")
                for tag in INPUT_BITS.keys():
                    results[tag] = "0"

        except Exception as e:
            logger.error(f"Falha na comunicação com o Altus: {e}")
            for tag in INPUT_BITS.keys():
                results[tag] = "0"
                
        # Atualiza o estado das saídas no frontend
        for tag, bit_index in OUTPUT_BITS.items():
            results[tag] = "1" if (self.current_output_byte & (1 << bit_index)) else "0"
            
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
                    
                    disconnected = []
                    for client in connected_clients:
                        try:
                            await client.send_text(json_update)
                        except Exception as e:
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
    try:
        while True:
            text = await websocket.receive_text()
            logger.info(f"Mensagem recebida via WebSocket: {text}")
            try:
                command = json.loads(text)
                if command.get("action") == "write":
                    plc_conn.write_tag(command.get("tag", ""), command.get("value", ""))
            except Exception as e:
                logger.error(f"Failed to parse incoming command: {e}")
    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.error(f"Error in websocket session: {e}")
    finally:
        if websocket in connected_clients:
            connected_clients.remove(websocket)