from dataclasses import asdict

from fastapi import APIRouter, HTTPException, Query

from app.estado import AppState
from app.modelos.comando import CommandMapping
from app.servicos.modbus_service import ModbusService
from app.servicos.mqtt_service import MQTTService


def criar_rotas(
    commands: dict[str, CommandMapping],
    modbus_service: ModbusService,
    mqtt_service: MQTTService,
    state: AppState,
) -> APIRouter:
    router = APIRouter()

    @router.get("/")
    def root():
        return {
            "message": "Altus MQTT Modbus Bridge API",
            "description": "API Python para receber comandos MQTT e escrever no CLP Altus via Modbus TCP.",
            "total_commands": len(commands),
        }

    @router.get("/health")
    def health():
        state_snapshot = state.snapshot()

        return {
            "api": "online",
            "mqtt_connected": mqtt_service.is_connected(),
            "modbus_connected": modbus_service.is_connected(),
            "last_message_at": state_snapshot["last_message_at"],
            "last_error": state_snapshot["last_error"],
        }

    @router.get("/mapping")
    def get_mapping():
        return {
            key: asdict(command)
            for key, command in commands.items()
        }

    @router.get("/state")
    def get_state():
        return state.snapshot()

    @router.post("/command/{kit}/{device_type}/{number}")
    def send_manual_command(
        kit: str,
        device_type: str,
        number: int,
        value: bool = Query(..., description="Valor booleano a ser enviado ao CLP"),
    ):
        """
        Endpoint HTTP para teste manual.

        Exemplos:

        POST /command/kit1/pushbutton/1?value=true
        POST /command/kit1/pushbutton/1?value=false
        """

        kit = normalize_kit(kit)
        device_type = device_type.lower()

        key = f"{kit}.{device_type}.{number}"

        command = commands.get(key)

        if command is None:
            raise HTTPException(
                status_code=404,
                detail=f"Comando não encontrado: {key}",
            )

        try:
            modbus_service.write_coil(
                command=command,
                value=value,
            )

            state.set_value(
                key=command.key,
                value=value,
            )

            return {
                "success": True,
                "command": asdict(command),
                "value": value,
            }

        except Exception as exc:
            state.set_error(str(exc))

            raise HTTPException(
                status_code=500,
                detail=str(exc),
            )

    return router


def normalize_kit(kit: str) -> str:
    kit = kit.lower().strip()

    if kit in ["1", "k1", "kit1"]:
        return "kit1"

    if kit in ["2", "k2", "kit2"]:
        return "kit2"

    return kit
