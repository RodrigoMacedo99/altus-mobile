import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.rotas import criar_rotas
from app.core.config import Settings
from app.core.mapeamento import build_command_mappings
from app.estado import AppState
from app.servicos.modbus_service import ModbusService
from app.servicos.mqtt_service import MQTTService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

settings = Settings()

commands = build_command_mappings(
    topic_prefix=settings.mqtt_topic_prefix,
)

state = AppState()

modbus_service = ModbusService(settings=settings)

mqtt_service = MQTTService(
    settings=settings,
    commands=commands,
    modbus_service=modbus_service,
    state=state,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        mqtt_service.start()

        logging.info(
            "API iniciada com sucesso. "
            "A conexão MQTT e a conexão Modbus serão tratadas de forma tolerante a falhas."
        )

        yield

    finally:
        mqtt_service.stop()
        modbus_service.close()

        logging.info("API finalizada")


app = FastAPI(
    title="Altus MQTT Modbus Bridge API",
    description="API Python para receber comandos MQTT e escrever no CLP Altus via Modbus TCP.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(
    criar_rotas(
        commands=commands,
        modbus_service=modbus_service,
        mqtt_service=mqtt_service,
        state=state,
    )
)
