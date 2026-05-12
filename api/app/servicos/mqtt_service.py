import json
import logging
from datetime import datetime

from paho.mqtt import client as mqtt

from app.core.config import Settings
from app.estado import AppState
from app.modelos.comando import CommandMapping
from app.servicos.modbus_service import ModbusService

logger = logging.getLogger("altus.mqtt")


class MQTTService:
    def __init__(
        self,
        settings: Settings,
        commands: dict[str, CommandMapping],
        modbus_service: ModbusService,
        state: AppState,
    ):
        self.settings = settings
        self.commands = commands
        self.commands_by_topic = {
            command.topic: command
            for command in commands.values()
        }
        self.modbus_service = modbus_service
        self.state = state
        self.client: mqtt.Client | None = None
        self.connected = False

    def start(self) -> None:
        """
        Inicializa o cliente MQTT.

        Importante:
        Aqui usamos connect_async para a API não cair caso o broker MQTT
        ainda não esteja rodando.
        """

        logger.info("Inicializando cliente MQTT")

        self.client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=self.settings.mqtt_client_id,
        )

        if self.settings.mqtt_username and self.settings.mqtt_password:
            self.client.username_pw_set(
                self.settings.mqtt_username,
                self.settings.mqtt_password,
            )

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

        self.client.reconnect_delay_set(
            min_delay=1,
            max_delay=30,
        )

        logger.info(
            "Tentando conectar ao broker MQTT em %s:%s",
            self.settings.mqtt_broker_host,
            self.settings.mqtt_broker_port,
        )

        try:
            self.client.connect_async(
                host=self.settings.mqtt_broker_host,
                port=self.settings.mqtt_broker_port,
                keepalive=60,
            )

            self.client.loop_start()

            logger.info(
                "Cliente MQTT iniciado. "
                "Se o broker estiver offline, a API continuará online e tentará reconectar."
            )

        except Exception as exc:
            logger.error("Erro ao iniciar cliente MQTT: %s", exc)
            self.connected = False

    def stop(self) -> None:
        if self.client is not None:
            logger.info("Parando cliente MQTT")

            try:
                self.publish_status("offline")
                self.client.loop_stop()
                self.client.disconnect()
            except Exception as exc:
                logger.warning("Erro ao parar cliente MQTT: %s", exc)

            self.connected = False

    def is_connected(self) -> bool:
        return self.connected

    def on_connect(self, client, userdata, connect_flags, reason_code, properties):
        self.connected = True

        logger.info("Conectado ao broker MQTT | reason_code=%s", reason_code)

        subscriptions = [
            (command.topic, self.settings.mqtt_qos)
            for command in self.commands.values()
        ]

        client.subscribe(subscriptions)

        logger.info("Inscrito em %s tópicos MQTT", len(subscriptions))

        self.publish_status(
            status="online",
            extra={
                "subscribed_topics": [
                    command.topic
                    for command in self.commands.values()
                ],
                "modbus_target": (
                    f"{self.settings.modbus_host}:"
                    f"{self.settings.modbus_port}"
                ),
            },
        )

    def on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties):
        self.connected = False

        logger.warning(
            "Desconectado do broker MQTT | reason_code=%s",
            reason_code,
        )

    def on_message(self, client, userdata, message):
        topic = message.topic
        payload = message.payload

        logger.info(
            "Mensagem MQTT recebida | topic=%s | payload=%s",
            topic,
            payload,
        )

        command = self.commands_by_topic.get(topic)

        if command is None:
            logger.warning("Tópico não mapeado: %s", topic)
            return

        try:
            value = self.parse_payload_to_bool(payload)

            self.modbus_service.write_coil(
                command=command,
                value=value,
            )

            self.state.set_value(
                key=command.key,
                value=value,
            )

            self.publish_ack(
                command=command,
                value=value,
                success=True,
            )

        except Exception as exc:
            error_message = str(exc)

            logger.exception("Erro ao processar mensagem MQTT")

            self.state.set_error(error_message)

            self.publish_ack(
                command=command,
                value=False,
                success=False,
                error=error_message,
            )

    def publish_status(self, status: str, extra: dict | None = None) -> None:
        if self.client is None:
            return

        if not self.connected:
            return

        payload = {
            "status": status,
            "timestamp": datetime.now().isoformat(),
        }

        if extra:
            payload.update(extra)

        topic = f"{self.settings.mqtt_topic_prefix}/api/status"

        self.client.publish(
            topic,
            json.dumps(payload),
            qos=self.settings.mqtt_qos,
            retain=False,
        )

    def publish_ack(
        self,
        command: CommandMapping,
        value: bool,
        success: bool,
        error: str | None = None,
    ) -> None:
        if self.client is None:
            return

        if not self.connected:
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

        ack_topic = f"{self.settings.mqtt_topic_prefix}/api/ack"

        self.client.publish(
            ack_topic,
            json.dumps(payload),
            qos=self.settings.mqtt_qos,
            retain=False,
        )

    @staticmethod
    def parse_payload_to_bool(payload: bytes) -> bool:
        """
        Aceita payloads simples ou JSON.

        Exemplos aceitos:

        1
        0
        true
        false
        on
        off

        {"value": true}
        {"pressed": true}
        {"state": 1}
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
                            return value.strip().lower() in [
                                "1",
                                "true",
                                "on",
                                "ligado",
                            ]

        except json.JSONDecodeError:
            pass

        normalized = raw.lower()

        if normalized in ["1", "true", "on", "ligado", "pressed", "pressionado"]:
            return True

        if normalized in ["0", "false", "off", "desligado", "released", "solto"]:
            return False

        raise ValueError(f"Payload inválido: {raw}")
    