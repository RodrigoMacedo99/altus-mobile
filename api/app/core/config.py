import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    # MQTT
    mqtt_broker_host: str = os.getenv("MQTT_BROKER_HOST", "localhost")
    mqtt_broker_port: int = int(os.getenv("MQTT_BROKER_PORT", "1883"))
    mqtt_username: str | None = os.getenv("MQTT_USERNAME") or None
    mqtt_password: str | None = os.getenv("MQTT_PASSWORD") or None
    mqtt_client_id: str = os.getenv("MQTT_CLIENT_ID", "altus-python-bridge")
    mqtt_topic_prefix: str = os.getenv("MQTT_TOPIC_PREFIX", "altus")
    mqtt_qos: int = 1

    # MODBUS TCP
    modbus_host: str = os.getenv("MODBUS_HOST", "192.168.0.10")
    modbus_port: int = int(os.getenv("MODBUS_PORT", "502"))
    modbus_timeout: float = float(os.getenv("MODBUS_TIMEOUT", "3"))

    # API
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))