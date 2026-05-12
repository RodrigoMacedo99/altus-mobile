import logging
from threading import Lock

from pymodbus.client import ModbusTcpClient

from app.core.config import Settings
from app.modelos.comando import CommandMapping

logger = logging.getLogger("altus.modbus")


class ModbusService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client: ModbusTcpClient | None = None
        self.lock = Lock()

    def connect(self) -> bool:
        """
        Tenta conectar ao CLP via Modbus TCP.

        Retorna True se conectou.
        Retorna False se não conseguiu conectar.
        """

        if self.client is None:
            self.client = ModbusTcpClient(
                host=self.settings.modbus_host,
                port=self.settings.modbus_port,
                timeout=self.settings.modbus_timeout,
            )

        if self.client.connected:
            return True

        logger.info(
            "Tentando conectar ao CLP Modbus em %s:%s",
            self.settings.modbus_host,
            self.settings.modbus_port,
        )

        try:
            connected = self.client.connect()
        except Exception as exc:
            logger.error("Erro ao tentar conectar ao CLP: %s", exc)
            return False

        if not connected:
            logger.warning(
                "Não foi possível conectar ao CLP em %s:%s",
                self.settings.modbus_host,
                self.settings.modbus_port,
            )
            return False

        logger.info("Conexão Modbus estabelecida com sucesso")

        return True

    def ensure_connection(self) -> None:
        """
        Garante que existe conexão antes de escrever no CLP.
        """

        connected = self.connect()

        if not connected:
            raise ConnectionError(
                f"Não foi possível conectar ao CLP em "
                f"{self.settings.modbus_host}:{self.settings.modbus_port}. "
                f"Verifique IP, porta, cabo de rede e configuração Modbus TCP do CLP."
            )

    def close(self) -> None:
        if self.client is not None:
            logger.info("Fechando conexão Modbus")
            self.client.close()

    def is_connected(self) -> bool:
        if self.client is None:
            return False

        return bool(self.client.connected)

    def write_coil(self, command: CommandMapping, value: bool) -> None:
        """
        Escreve o valor de um comando em um coil do CLP.
        """

        with self.lock:
            self.ensure_connection()

            logger.info(
                "Escrevendo no CLP | comando=%s | coil=%s | valor=%s",
                command.key,
                command.coil_address,
                value,
            )

            result = self.client.write_coil(
                address=command.coil_address,
                value=value,
            )

            if result.isError():
                raise RuntimeError(
                    f"Erro Modbus ao escrever no coil "
                    f"{command.coil_address}: {result}"
                )
