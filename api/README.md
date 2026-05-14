# API

API do sistema.

## Docker

Suba a API e o broker MQTT com:

```bash
docker compose up --build
```

O Compose levanta dois containers:

- `mosquitto`, com o broker MQTT na porta `1883`
- `api`, com a API FastAPI na porta `8000`

Dentro da rede do Docker, a API conecta no broker pelo hostname `mosquitto`.
