from datetime import datetime
from threading import Lock


class AppState:
    def __init__(self):
        self._lock = Lock()
        self.last_values: dict[str, bool] = {}
        self.last_message_at: str | None = None
        self.last_error: str | None = None

    def set_value(self, key: str, value: bool) -> None:
        with self._lock:
            self.last_values[key] = value
            self.last_message_at = datetime.now().isoformat()
            self.last_error = None

    def set_error(self, error: str) -> None:
        with self._lock:
            self.last_error = error

    def snapshot(self) -> dict:
        with self._lock:
            return {
                "last_values": self.last_values,
                "last_message_at": self.last_message_at,
                "last_error": self.last_error,
            }