**Altus MQTT ↔ Modbus Bridge — API**

Visão geral
----------

Esta pasta contém a API que faz a ponte entre o app mobile (via MQTT) e o CLP Altus (via Modbus).
O propósito principal é: receber mensagens MQTT publicadas pelo app mobile, traduzir para
endereçamento de coils Modbus e escrever no CLP; publicar confirmações/estado de volta ao broker.

Arquitetura e componentes (localização dos arquivos)
--------------------------------------------------

- **Ponto de entrada:** `run.py` — inicia o servidor Uvicorn em desenvolvimento.
- **Aplicação FastAPI:** [app/main.py](app/main.py) — cria a app, configura logging e gerencia o ciclo de vida
	(inicia `MQTTService` no startup, finaliza serviços no shutdown).
- **Rotas HTTP:** [app/api/rotas.py](app/api/rotas.py) — endpoints para health, mapping, state e envio manual de comando.
- **Serviços:**
	- `app/servicos/mqtt_service.py` — cliente MQTT (paho-mqtt). Inscrições, parsing de payloads, ack/status.
	- `app/servicos/modbus_service.py` — cliente Modbus. Suporta Modbus RTU (serial RS-485) e Modbus TCP.
- **Core/configuração:** [app/core/config.py](app/core/config.py) — todas as variáveis de ambiente e defaults.
- **Mapeamento de comandos:** [app/core/mapeamento.py](app/core/mapeamento.py) — gera `CommandMapping` para tópicos e coils.
- **Modelos:** [app/modelos/comando.py](app/modelos/comando.py) — `CommandMapping` (dataclass).
- **Estado compartilhado:** [app/estado.py](app/estado.py) — guarda últimos valores, timestamp e último erro.

Fluxo de dados (runtime)
-----------------------

1. Startup: `app/main.py` instancia `MQTTService` e `ModbusService`. `MQTTService.start()` conecta ao broker
	 assíncronamente e inicia o loop de mensagens.
2. O app mobile publica um comando em um tópico, por exemplo:
	 `altus/kit1/pushbutton/1`.
3. `MQTTService.on_message` recebe a mensagem, converte o payload para booleano via
	 `parse_payload_to_bool`, localiza o `CommandMapping` correspondente e chama
	 `ModbusService.write_coil(command, value)`.
4. `ModbusService` garante conexão (RTU serial ou TCP) e escreve o coil no CLP.
5. `MQTTService` publica um ack em `altus/api/ack` com informações sobre sucesso/erro e atualiza `AppState`.

Modos de transporte Modbus
-------------------------

- **RTU (serial / RS-485):** se a variável de ambiente `MODBUS_SERIAL_PORT` estiver definida, a API
	usará `pymodbus.client.ModbusSerialClient` para comunicação direta via serial (ex.: `COM3` ou `/dev/ttyUSB0`).
	Configure também `MODBUS_SERIAL_BAUDRATE`, `MODBUS_SERIAL_PARITY`, `MODBUS_SERIAL_STOPBITS`, `MODBUS_SERIAL_BYTESIZE`.
- **TCP:** fallback quando `MODBUS_SERIAL_PORT` não estiver definido; usa `pymodbus.client.ModbusTcpClient` e
	as variáveis `MODBUS_HOST`, `MODBUS_PORT`, `MODBUS_TIMEOUT`.

Endpoints HTTP principais
------------------------

- `GET /` — resumo e total de comandos mapeados.
- `GET /health` — estado da API, `mqtt_connected`, `modbus_connected`, `last_message_at`, `last_error`.
- `GET /mapping` — retorna todos os `CommandMapping` (tópicos e endereços de coil).
- `GET /state` — snapshot do `AppState` (últimos valores e timestamps).
- `POST /command/{kit}/{device_type}/{number}?value={true|false}` — endpoint de teste/manual para escrever um coil.

Formato de tópicos e mapeamento
-------------------------------

O mapeamento gerado por [app/core/mapeamento.py](app/core/mapeamento.py) cria 16 entradas:

- `kit1.pushbutton.1..4` -> coils 0..3
- `kit1.switch.1..4` -> coils 4..7
- `kit2.pushbutton.1..4` -> coils 8..11
- `kit2.switch.1..4` -> coils 12..15

O tópico MQTT padrão é `{MQTT_TOPIC_PREFIX}/{kit}/{device_type}/{number}` — ex.: `altus/kit1/pushbutton/1`.

Payloads aceitos (exemplos) — `parse_payload_to_bool`
---------------------------------------------------

- Simples: `1`, `0`, `true`, `false`, `on`, `off` (strings ou bytes)
- JSON: `{ "value": true }`, `{ "pressed": true }`, `{ "state": 1 }`

Configuração (variáveis de ambiente)
-----------------------------------

Recomenda-se documentar esses valores no ambiente de deploy ou no `.env`:

- MQTT
	- `MQTT_BROKER_HOST` (default: `localhost`)
	- `MQTT_BROKER_PORT` (default: `1883`)
	- `MQTT_USERNAME`, `MQTT_PASSWORD` (opcionais)
	- `MQTT_CLIENT_ID` (default: `altus-python-bridge`)
	- `MQTT_TOPIC_PREFIX` (default: `altus`)
	- `MQTT_QOS` (default: `1`)

- Modbus RTU (RS-485)
	- `MODBUS_SERIAL_PORT` (ex.: `COM3` ou `/dev/ttyUSB0`)  — se definido, ativa RTU
	- `MODBUS_SERIAL_BAUDRATE` (default: `19200`)
	- `MODBUS_SERIAL_PARITY` (default: `N`)
	- `MODBUS_SERIAL_STOPBITS` (default: `1`)
	- `MODBUS_SERIAL_BYTESIZE` (default: `8`)
	- `MODBUS_SERIAL_METHOD` (default: `rtu`)

- Modbus TCP (fallback)
	- `MODBUS_HOST` (default: `192.168.0.10`)
	- `MODBUS_PORT` (default: `502`)
	- `MODBUS_TIMEOUT` (default: `3`)

- API
	- `API_HOST` (default: `0.0.0.0`)
	- `API_PORT` (default: `8000`)

Execução local (desenvolvimento)
--------------------------------

1. Criar e ativar venv e instalar dependências:

```bash
python -m venv .venv
.venv\\Scripts\\Activate.ps1  # PowerShell (Windows)
pip install -r requirements.txt
```

2. Rodar em modo desenvolvimento (autoreload):

```bash
python run.py
# ou
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

3. Exemplo de variáveis para RS-485 (PowerShell):

```powershell
$env:MODBUS_SERIAL_PORT="COM3"
$env:MODBUS_SERIAL_BAUDRATE="19200"
$env:MODBUS_SERIAL_PARITY="N"
```

Testes e endpoints úteis
------------------------

- `GET http://localhost:8000/health` — checar `mqtt_connected` e `modbus_connected`.
- `GET http://localhost:8000/mapping` — ver os tópicos e endereços de coils.
- `POST http://localhost:8000/command/kit1/pushbutton/1?value=true` — testar escrita manual.
- Para testar MQTT manualmente (mosquitto client):
	```bash
	mosquitto_pub -h localhost -t "altus/kit1/pushbutton/1" -m "1"
	```

Publicação de ACK/status
------------------------

- A API publica em `altus/api/ack` um JSON com os campos: `command`, `kit`, `device_type`, `number`,
	`topic`, `coil_address`, `value`, `success`, `error`, `timestamp`.
- Status da API em `altus/api/status` com `status` = `online`/`offline` e metadados.

Boas práticas e recomendações
----------------------------

- Segurança: os endpoints HTTP atualmente não têm autenticação — se expor a rede, proteger com
	autenticação, rede privada ou firewall.
- Logging: `app/main.py` configura `logging` em nível `INFO`. Use `DEBUG` para troubleshooting.
- Linter/CI: adicione `ruff` ou `flake8` e `pre-commit` para evitar código morto.
- Testes: adicione testes unitários para `parse_payload_to_bool` e para mapeamento de comandos.

Troubleshooting rápido
----------------------

- Se `modbus_connected` em `/health` for `false`:
	- Verifique `MODBUS_SERIAL_PORT` (RTU) ou `MODBUS_HOST`/`MODBUS_PORT` (TCP).
	- Se RTU, confirme permissões de acesso à porta serial e que nenhum outro processo esteja usando-a.
- Se MQTT não conectar:
	- Verifique `MQTT_BROKER_HOST`/`MQTT_BROKER_PORT` e credenciais.
	- O broker `mosquitto` pode ser levantado via `docker compose up --build` (ver `api/docker-compose.yml`).

Onde documentar mais
---------------------

- Exemplos JSON de payload mais complexos e casos de borda em `docs/payloads.md` (sugestão).
- Diagrama de arquitetura (Mermaid) em `docs/architecture.md`.

Notas finais
-----------

Este README substitui o guia mínimo anterior e contém a visão arquitetural que seu colega pode usar
para compor a documentação formal. Posso gerar um diagrama Mermaid e/ou um arquivo `docs/ARCHITECTURE.md`
com seções divididas por público (engenharia, operação, QA) se desejar.

