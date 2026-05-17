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

    # MODBUS RTU (serial, RS-485)
    # If `modbus_serial_port` is set, the application will try to use Modbus RTU
    # over the given serial port instead of Modbus TCP.
    modbus_serial_port: str | None = os.getenv("MODBUS_SERIAL_PORT") or None
    modbus_serial_baudrate: int = int(os.getenv("MODBUS_SERIAL_BAUDRATE", "19200"))
    modbus_serial_parity: str = os.getenv("MODBUS_SERIAL_PARITY", "N")
    modbus_serial_stopbits: int = int(os.getenv("MODBUS_SERIAL_STOPBITS", "1"))
    modbus_serial_bytesize: int = int(os.getenv("MODBUS_SERIAL_BYTESIZE", "8"))
    modbus_serial_method: str = os.getenv("MODBUS_SERIAL_METHOD", "rtu")

    # API
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))



## Defina as variáveis de ambiente para usar RS-485
# $env:MODBUS_SERIAL_PORT="COM3"
# $env:MODBUS_SERIAL_BAUDRATE="19200"
# $env:MODBUS_SERIAL_PARITY="N"
# $env:MODBUS_SERIAL_STOPBITS="1"
# $env:MODBUS_SERIAL_BYTESIZE="8"