import json
import logging
import os
import threading
from contextlib import asynccontextmanager
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Dict, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from paho.mqtt import client as mqtt
from pymodbus.client import ModbusTcpClient

load_dotenv()

# ============================================================
# CONFIGURAÇÕES GERAIS
# ============================================================

MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "localhost")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", "1883"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME") or None
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD") or None
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "altus-python-bridge")
MQTT_TOPIC_PREFIX = os.getenv("MQTT_TOPIC_PREFIX", "altus")
MQTT_QOS = 1

MODBUS_HOST = os.getenv("MODBUS_HOST", "192.168.0.10")
MODBUS_PORT = int(os.getenv("MODBUS_PORT", "502"))
MODBUS_TIMEOUT = float(os.getenv("MODBUS_TIMEOUT", "3"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("altus-mqtt-modbus-api")


# ============================================================
# MODELO DE COMANDO
# ============================================================

@dataclass
class CommandMapping:
    key: str
    kit: str
    device_type: str
    number: int
    topic: str
    coil_address: int
    description: str


def build_command_mappings() -> Dict[str, CommandMapping]:
    """
    Mapeamento dos 16 comandos para coils Modbus.

    Endereçamento adotado:
    - Kit 1 pushbuttons: coils 0 a 3
    - Kit 1 switches:    coils 4 a 7
    - Kit 2 pushbuttons: coils 8 a 11
    - Kit 2 switches:    coils 12 a 15

    Como o Kit 2 depende do Kit 1, a API sempre escreve no Kit 1.
    Os coils 8 a 15 representam comandos que o Kit 1 deverá repassar ao Kit 2.
    """

    mappings: Dict[str, CommandMapping] = {}

    base_addresses = {
        ("kit1", "pushbutton"): 0,
        ("kit1", "switch"): 4,
        ("kit2", "pushbutton"): 8,
        ("kit2", "switch"): 12,
    }

    for kit in ["kit1", "kit2"]:
        for device_type in ["pushbutton", "switch"]:
            base = base_addresses[(kit, device_type)]

            for number in range(1, 5):
                key = f"{kit}.{device_type}.{number}"
                topic = f"{MQTT_TOPIC_PREFIX}/{kit}/{device_type}/{number}"
                coil_address = base + (number - 1)

                mappings[key] = CommandMapping(
                    key=key,
                    kit=kit,
                    device_type=device_type,
                    number=number,
                    topic=topic,
                    coil_address=coil_address,
                    description=f"{device_type} {number} do {kit}",
                )

    return mappings


COMMANDS = build_command_mappings()
COMMANDS_BY_TOPIC = {command.topic: command for command in COMMANDS.values()}


# ============================================================
# ESTADO DA APLICAÇÃO
# ============================================================

modbus_lock = threading.Lock()
modbus_client: Optional[ModbusTcpClient] = None
mqtt_client: Optional[mqtt.Client] = None

last_values: Dict[str, bool] = {}
last_message_at: Optional[str] = None
last_error: Optional[str] = None


# ============================================================
# FUNÇÕES MODBUS
# ============================================================

def connect_modbus() -> None:
    """
    Cria conexão com o CLP via Modbus TCP.
    """
    global modbus_client

    if modbus_client is None:
        modbus_client = ModbusTcpClient(
            host=MODBUS_HOST,
            port=MODBUS_PORT,
            timeout=MODBUS_TIMEOUT,
        )

    if not modbus_client.connected:
        logger.info("Conectando ao CLP Modbus em %s:%s", MODBUS_HOST, MODBUS_PORT)
        connected = modbus_client.connect()

        if not connected:
            raise ConnectionError(
                f"Não foi possível conectar ao CLP em {MODBUS_HOST}:{MODBUS_PORT}"
            )


def close_modbus() -> None:
    """
    Fecha conexão Modbus.
    """
    global modbus_client

    if modbus_client is not None:
        logger.info("Fechando conexão Modbus")
        modbus_client.close()


def write_coil_to_plc(command: CommandMapping, value: bool) -> None:
    """
    Escreve um valor booleano em um coil do CLP.
    """
    global last_error

    with modbus_lock:
        connect_modbus()

        logger.info(
            "Escrevendo no CLP | comando=%s | coil=%s | valor=%s",
            command.key,
            command.coil_address,
            value,
        )

        result = modbus_client.write_coil(
            address=command.coil_address,
            value=value,
        )

        if result.isError():
            raise RuntimeError(
                f"Erro Modbus ao escrever no coil {command.coil_address}: {result}"
            )

        last_values[command.key] = value
        last_error = None


# ============================================================
# PARSER DAS MENSAGENS MQTT
# ============================================================

def parse_payload_to_bool(payload: bytes) -> bool:
    """
    Aceita payloads simples ou JSON.

    Payloads aceitos:
    - "1"
    - "0"
    - "true"
    - "false"
    - "on"
    - "off"
    - {"value": true}
    - {"pressed": true}
    - {"state": 1}
    """

    raw = payload.decode("utf-8").strip()

    try:
        data = json.loads(raw)

        if isinstance(data, bool):
            return data

        if isinstance(data, int):
            return data == 1

        if isinstance(data, dict):
            for key in ["value", "pressed", "state", "on"]:
                if key in data:
                    value = data[key]

                    if isinstance(value, bool):
                        return value

                    if isinstance(value, int):
                        return value == 1

                    if isinstance(value, str):
                        return value.strip().lower() in ["1", "true", "on", "ligado"]

    except json.JSONDecodeError:
        pass

    normalized = raw.lower()

    if normalized in ["1", "true", "on", "ligado", "pressed", "pressionado"]:
        return True

    if normalized in ["0", "false", "off", "desligado", "released", "solto"]:
        return False

    raise ValueError(f"Payload inválido: {raw}")


# ============================================================
# FUNÇÕES MQTT
# ============================================================

def publish_api_status(status: str, extra: Optional[dict] = None) -> None:
    """
    Publica status da API no broker MQTT.
    """
    if mqtt_client is None:
        return

    payload = {
        "status": status,
        "timestamp": datetime.now().isoformat(),
    }

    if extra:
        payload.update(extra)

    topic = f"{MQTT_TOPIC_PREFIX}/api/status"
    mqtt_client.publish(topic, json.dumps(payload), qos=MQTT_QOS, retain=False)


def publish_ack(command: CommandMapping, value: bool, success: bool, error: Optional[str] = None) -> None:
    """
    Publica confirmação de processamento de comando.
    """
    if mqtt_client is None:
        return

    payload = {
        "command": command.key,
        "kit": command.kit,
        "device_type": command.device_type,
        "number": command.number,
        "topic": command.topic,
        "coil_address": command.coil_address,
        "value": value,
        "success": success,
        "error": error,
        "timestamp": datetime.now().isoformat(),
    }

    ack_topic = f"{MQTT_TOPIC_PREFIX}/api/ack"
    mqtt_client.publish(ack_topic, json.dumps(payload), qos=MQTT_QOS, retain=False)


def on_connect(client, userdata, connect_flags, reason_code, properties):
    """
    Callback chamado quando a API conecta no broker MQTT.
    A assinatura segue a Callback API v2 do paho-mqtt.
    """
    logger.info("Conectado ao broker MQTT | reason_code=%s", reason_code)

    subscriptions = [(command.topic, MQTT_QOS) for command in COMMANDS.values()]
    client.subscribe(subscriptions)

    logger.info("Inscrito em %s tópicos MQTT", len(subscriptions))

    publish_api_status(
        "online",
        {
            "subscribed_topics": [command.topic for command in COMMANDS.values()],
            "modbus_target": f"{MODBUS_HOST}:{MODBUS_PORT}",
        },
    )


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    logger.warning("Desconectado do broker MQTT | reason_code=%s", reason_code)


def on_message(client, userdata, message):
    """
    Callback chamado para cada mensagem MQTT recebida.
    No paho-mqtt, o callback de mensagem recebe client, userdata e message.
    """

    global last_message_at, last_error

    topic = message.topic
    payload = message.payload

    logger.info("Mensagem MQTT recebida | topic=%s | payload=%s", topic, payload)

    command = COMMANDS_BY_TOPIC.get(topic)

    if command is None:
        logger.warning("Tópico não mapeado: %s", topic)
        return

    try:
        value = parse_payload_to_bool(payload)

        write_coil_to_plc(command, value)

        last_message_at = datetime.now().isoformat()

        publish_ack(
            command=command,
            value=value,
            success=True,
        )

    except Exception as exc:
        last_error = str(exc)

        logger.exception("Erro ao processar mensagem MQTT")

        try:
            publish_ack(
                command=command,
                value=False,
                success=False,
                error=str(exc),
            )
        except Exception:
            logger.exception("Erro ao publicar ACK de falha")


def start_mqtt() -> None:
    """
    Inicializa o cliente MQTT e conecta no broker.
    """

    global mqtt_client

    logger.info("Inicializando cliente MQTT")

    mqtt_client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=MQTT_CLIENT_ID,
    )

    if MQTT_USERNAME and MQTT_PASSWORD:
        mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    mqtt_client.on_connect = on_connect
    mqtt_client.on_disconnect = on_disconnect
    mqtt_client.on_message = on_message

    mqtt_client.reconnect_delay_set(min_delay=1, max_delay=30)

    logger.info("Conectando ao broker MQTT em %s:%s", MQTT_BROKER_HOST, MQTT_BROKER_PORT)

    mqtt_client.connect(
        host=MQTT_BROKER_HOST,
        port=MQTT_BROKER_PORT,
        keepalive=60,
    )

    mqtt_client.loop_start()


def stop_mqtt() -> None:
    """
    Para o cliente MQTT.
    """
    global mqtt_client

    if mqtt_client is not None:
        logger.info("Parando cliente MQTT")
        publish_api_status("offline")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()


# ============================================================
# FASTAPI
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        connect_modbus()
        start_mqtt()

        logger.info("API iniciada com sucesso")

        yield

    finally:
        stop_mqtt()
        close_modbus()
        logger.info("API finalizada")


app = FastAPI(
    title="Altus MQTT Modbus Bridge API",
    description="API Python para receber comandos MQTT e escrever no CLP Altus via Modbus TCP.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {
        "message": "Altus MQTT Modbus Bridge API",
        "mqtt_broker": f"{MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}",
        "modbus_target": f"{MODBUS_HOST}:{MODBUS_PORT}",
        "total_commands": len(COMMANDS),
    }


@app.get("/health")
def health():
    modbus_connected = False

    try:
        if modbus_client is not None:
            modbus_connected = modbus_client.connected
    except Exception:
        modbus_connected = False

    return {
        "api": "online",
        "mqtt_broker": f"{MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}",
        "modbus_target": f"{MODBUS_HOST}:{MODBUS_PORT}",
        "modbus_connected": modbus_connected,
        "last_message_at": last_message_at,
        "last_error": last_error,
    }


@app.get("/mapping")
def get_mapping():
    return {
        key: asdict(command)
        for key, command in COMMANDS.items()
    }


@app.get("/state")
def get_state():
    return {
        "last_values": last_values,
        "last_message_at": last_message_at,
        "last_error": last_error,
    }


@app.post("/command/{kit}/{device_type}/{number}")
def send_manual_command(
    kit: str,
    device_type: str,
    number: int,
    value: bool = Query(..., description="Valor booleano a ser enviado ao CLP"),
):
    """
    Endpoint HTTP para teste manual.

    Exemplo:
    POST /command/kit1/pushbutton/1?value=true
    POST /command/kit1/pushbutton/1?value=false
    """

    kit = kit.lower()
    device_type = device_type.lower()

    if kit in ["1", "k1"]:
        kit = "kit1"

    if kit in ["2", "k2"]:
        kit = "kit2"

    key = f"{kit}.{device_type}.{number}"

    command = COMMANDS.get(key)

    if command is None:
        raise HTTPException(
            status_code=404,
            detail=f"Comando não encontrado: {key}",
        )

    try:
        write_coil_to_plc(command, value)

        return {
            "success": True,
            "command": asdict(command),
            "value": value,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )