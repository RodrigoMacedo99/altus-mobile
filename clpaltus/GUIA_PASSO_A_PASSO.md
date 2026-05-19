# Guia: Conectar App → CLP Mestre (MQTT) → CLP Escravo (Modbus RS-485)

Os arquivos de código estão em `clpaltus/codigo/`:
- `clp_mestre/` → programas do primeiro CLP (gateway MQTT ↔ Modbus)
- `clp_escravo/` → programas do segundo CLP (executa saídas físicas)

---

## Fluxo completo de comunicação

```
[App Android]
     | pressiona botão → publica "1" ou "0"
     ↓
[Broker Mosquitto] ← rodando no PC Windows
     ↓
[CLP Mestre - XP340]          ← gateway, não aciona saídas próprias
     | MQTT_RECEBER: converte payload em CMD_Q00-Q15 (BOOL)
     | MODBUS_GATEWAY: empacota em MB_CMD_KIT1/KIT2 (WORD)
     ↓ RS-485 / Modbus RTU FC16 (escreve)
[CLP Escravo]
     | ESCRAVO_SAIDAS: extrai bits → Q00-Q15 ligam/desligam
     | ESCRAVO_RETORNO: lê estado real → MB_FB_KIT1/KIT2
     ↑ RS-485 / Modbus RTU FC03 (lê retorno)
[CLP Mestre]
     | MODBUS_GATEWAY: desempacota MB_FB → PUBS_PAYLOADS
     | MQTT: publica retorno nos tópicos
     ↑
[Broker Mosquitto]
     ↑
[App Android] ← LEDs acendem/apagam com o estado real do escravo
```

---

## Antes de começar

Você vai precisar de:
- Dois CLPs da série Nexto (XP340 ou similar) conectados por cabo RS-485
- MasterTool instalado com dois projetos separados (um por CLP)
- Mosquitto instalado no PC
- CLP Mestre conectado ao PC via rede (Ethernet)

---

## PARTE 1 — Configurar o CLP MESTRE no MasterTool

> Abra (ou crie) o projeto do **CLP Mestre** no MasterTool.

### Passo 1 — Adicionar a biblioteca LibMQTT

1. No painel **Devices**, dê **duplo clique** em **Library Manager**
2. Clique em **"Add Library"**
3. **Digite:** `mqtt` na caixa de busca
4. Selecione **LibMQTT** e clique **OK**
5. Clique em **LibMQTT** na lista para selecioná-la
6. Aba **"Library Parameters"** → ajuste:
   - `gc_uMaxSubs` = `50`
   - `gc_uMaxPubs` = `50`

---

### Passo 2 — Criar a pasta MQTT

1. Botão direito em **Application** → **Add Object** → **Folder**
2. **Nome:** `MQTT` → OK

---

### Passo 3 — Criar as GVLs

**GVL_MQTT:**
1. Botão direito em **Application** → **Add Object** → **Global Variable List**
2. **Nome:** `GVL_MQTT` → OK
3. Abra `clpaltus/codigo/clp_mestre/GVL_MQTT.st` no Bloco de Notas
4. **Ctrl+A** → **Ctrl+C** → cole no MasterTool (**Ctrl+A** → **Ctrl+V**)
5. **Ctrl+S**

**GVL_MODBUS:**
1. Botão direito em **Application** → **Add Object** → **Global Variable List**
2. **Nome:** `GVL_MODBUS` → OK
3. Abra `clpaltus/codigo/clp_mestre/GVL_MODBUS.st` no Bloco de Notas
4. Cole o conteúdo → **Ctrl+S**

---

### Passo 4 — Criar os programas (POUs)

Para cada programa abaixo, faça:
> Botão direito na pasta **MQTT** → **Add Object** → **POU**
> Tipo: **Program** | Linguagem: **Structured Text (ST)** → OK

| Nome do POU | Arquivo para copiar |
|---|---|
| `MQTT_RECEBER` | `clp_mestre/MQTT_RECEBER.st` |
| `MODBUS_GATEWAY` | `clp_mestre/MODBUS_GATEWAY.st` |
| `MQTT` | `clp_mestre/MQTT.st` |

Para o POU `MQTT`, atenção especial:
- Cole a seção **VAR** na área de variáveis (parte de cima)
- Cole o **CÓDIGO** na área de código (parte de baixo)
- **Troque o IP** na linha `sHostname := '192.168.X.X'`
  → Para descobrir o IP: abra o CMD e digite `ipconfig`, veja "Endereço IPv4"

---

### Passo 5 — Adicionar os programas na Task do Mestre

1. Expanda **Task Configuration** → **MainTask**
2. Botão direito em **MainTask** → **"Add Call"**
3. Adicione na seguinte ordem (ordem importa):
   1. `MQTT_RECEBER`
   2. `MODBUS_GATEWAY`
   3. `MQTT`

---

### Passo 6 — Configurar RS-485 Modbus Master (hardware)

1. No painel **Devices**, expanda o XP340 e dê **duplo clique** em **COM 1**
2. Em **"Protocol"**, selecione **"Modbus RTU Master"**
3. Configure:

   | Parâmetro | Valor |
   |-----------|-------|
   | Baud Rate | `9600` |
   | Data Bits | `8` |
   | Parity    | `None` |
   | Stop Bits | `1` |
   | Interface | `RS-485` |

4. Clique **OK**

---

### Passo 7 — Adicionar o CLP escravo na rede Modbus

1. Botão direito em **COM 1** → **"Add Device"**
2. Selecione **"Modbus RTU Slave Device"** → **OK**
3. Dê **duplo clique** no escravo criado
4. **Slave Address:** `1`

---

### Passo 8 — Mapear os registradores Modbus

Ainda na configuração do escravo, abra a aba **"Modbus Slave Channel"** ou **"I/O Mapping"**:

**Canal de ESCRITA (mestre → escravo):**
1. Clique **"Add Channel"** → **FC16 – Write Multiple Registers**
2. Start Address: `0` | Length: `2`
3. Na coluna **Variable**, mapeie:
   - Registrador 0 → `GVL_MODBUS.MB_CMD_KIT1`
   - Registrador 1 → `GVL_MODBUS.MB_CMD_KIT2`

**Canal de LEITURA (mestre lê retorno do escravo):**
1. Clique **"Add Channel"** → **FC03 – Read Holding Registers**
2. Start Address: `2` | Length: `2`
3. Na coluna **Variable**, mapeie:
   - Registrador 2 → `GVL_MODBUS.MB_FB_KIT1`
   - Registrador 3 → `GVL_MODBUS.MB_FB_KIT2`

4. **Ctrl+S**

---

### Passo 9 — Carregar o programa no CLP Mestre

1. **F11** para compilar
2. **F8** para conectar ao CLP
3. Confirme o download → **Yes**
4. **F5** para iniciar

---

## PARTE 2 — Configurar o CLP ESCRAVO no MasterTool

> Abra (ou crie) o projeto do **CLP Escravo** no MasterTool.
> É um projeto separado do mestre.

### Passo 10 — Criar a GVL do escravo

1. Botão direito em **Application** → **Add Object** → **Global Variable List**
2. **Nome:** `GVL_ESCRAVO` → OK
3. Abra `clpaltus/codigo/clp_escravo/GVL_ESCRAVO.st` no Bloco de Notas
4. Cole o conteúdo → **Ctrl+S**

---

### Passo 11 — Criar os programas do escravo

| Nome do POU | Arquivo para copiar |
|---|---|
| `ESCRAVO_SAIDAS` | `clp_escravo/ESCRAVO_SAIDAS.st` |
| `ESCRAVO_RETORNO` | `clp_escravo/ESCRAVO_RETORNO.st` |

---

### Passo 12 — Adicionar os programas na Task do Escravo

1. Expanda **Task Configuration** → **MainTask**
2. Adicione na ordem:
   1. `ESCRAVO_SAIDAS`
   2. `ESCRAVO_RETORNO`

---

### Passo 13 — Configurar RS-485 Modbus Slave (hardware do escravo)

1. Dê **duplo clique** em **COM 1** do escravo
2. Em **"Protocol"**, selecione **"Modbus RTU Slave"**
3. Configure **o mesmo** Baud Rate, Data Bits, Parity e Stop Bits do mestre
4. **Slave Address:** `1`

Mapeie os registradores do escravo:

5. Aba **"I/O Mapping"**:
   - Registrador endereço 0 → `GVL_ESCRAVO.MB_CMD_KIT1`
   - Registrador endereço 1 → `GVL_ESCRAVO.MB_CMD_KIT2`
   - Registrador endereço 2 → `GVL_ESCRAVO.MB_FB_KIT1`
   - Registrador endereço 3 → `GVL_ESCRAVO.MB_FB_KIT2`

6. **Ctrl+S**

---

### Passo 14 — Carregar o programa no CLP Escravo

1. **F11** → **F8** → **Yes** → **F5**

---

### Passo 15 — Ligar o cabo RS-485

```
CLP Mestre (COM1)          CLP Escravo (COM1)
   Pino A    ←——————————→    Pino A
   Pino B    ←——————————→    Pino B
   GND       ←——————————→    GND  (recomendado)
```

> Consulte o manual do XP340 para identificar os pinos A, B e GND no conector COM1.

---

## PARTE 3 — Configurar o Mosquitto no PC

### Passo 16 — Copiar o arquivo de configuração

1. Abra o **Explorador de Arquivos**
2. Vá até `C:\Sistemas\Faculdade\altus-mobile\infra\mosquitto\`
3. Copie `mosquitto.conf` e cole em `C:\Program Files\mosquitto\`

Crie as pastas necessárias (abra o CMD e execute):
```
mkdir C:\mosquitto\data
mkdir C:\mosquitto\log
```

---

### Passo 17 — Iniciar o Mosquitto

1. Abra o Explorador em `C:\Program Files\mosquitto`
2. Clique na barra de endereço, **digite** `cmd`, pressione **Enter**
3. **Digite:**
   ```
   mosquitto -v
   ```
4. Deixe essa janela aberta

---

## PARTE 4 — Testar

### Passo 18 — Testar pelo CMD

Abra outra janela de CMD em `C:\Program Files\mosquitto`:

**Ligar saída Q00 no escravo:**
```
mosquitto_pub -h localhost -p 1883 -t "altus/kit1/pushbutton/1" -m "1"
```

**Desligar:**
```
mosquitto_pub -h localhost -p 1883 -t "altus/kit1/pushbutton/1" -m "0"
```

**O que deve acontecer:**
1. Mestre recebe via MQTT → `CMD_Q00 = TRUE`
2. Mestre escreve via Modbus RS-485 → `MB_CMD_KIT1.0 = TRUE`
3. Escravo lê → `Q00 = TRUE` (saída física liga)
4. Escravo retorna → `MB_FB_KIT1.0 = TRUE`
5. Mestre lê o retorno → publica `"1"` em `altus/kit1/pushbutton/1`
6. App recebe → `kit1Led1` acende (verde)

---

## Resumo dos arquivos

### CLP Mestre (gateway MQTT ↔ Modbus)
| Arquivo | Função |
|---------|--------|
| `clp_mestre/GVL_MQTT.st` | Tópicos e variáveis MQTT |
| `clp_mestre/GVL_MODBUS.st` | Registradores de comando e retorno |
| `clp_mestre/MQTT_RECEBER.st` | Converte payload MQTT → CMD_Q* (BOOL) |
| `clp_mestre/MODBUS_GATEWAY.st` | Empacota comandos para RS-485; desempacota retorno para MQTT |
| `clp_mestre/MQTT.st` | Conexão MQTT (subscribe + publish) |

### CLP Escravo (executa as saídas físicas)
| Arquivo | Função |
|---------|--------|
| `clp_escravo/GVL_ESCRAVO.st` | Registradores Modbus do escravo |
| `clp_escravo/ESCRAVO_SAIDAS.st` | Extrai bits recebidos → Q00-Q15 (saídas físicas) |
| `clp_escravo/ESCRAVO_RETORNO.st` | Empacota estado real das saídas → retorno ao mestre |

---

## Mapeamento completo

| Botão/Chave no App | Tópico MQTT | CMD no Mestre | Saída no Escravo | LED no App |
|---|---|---|---|---|
| Kit1 Botão 1 | `altus/kit1/pushbutton/1` | CMD_Q00 | Q00 | kit1Led1 |
| Kit1 Botão 2 | `altus/kit1/pushbutton/2` | CMD_Q01 | Q01 | kit1Led2 |
| Kit1 Botão 3 | `altus/kit1/pushbutton/3` | CMD_Q02 | Q02 | kit1Led3 |
| Kit1 Botão 4 | `altus/kit1/pushbutton/4` | CMD_Q03 | Q03 | kit1Led4 |
| Kit1 Switch 1 | `altus/kit1/switch/1` | CMD_Q04 | Q04 | kit1Led5 |
| Kit1 Switch 2 | `altus/kit1/switch/2` | CMD_Q05 | Q05 | kit1Led6 |
| Kit1 Switch 3 | `altus/kit1/switch/3` | CMD_Q06 | Q06 | kit1Led7 |
| Kit1 Switch 4 | `altus/kit1/switch/4` | CMD_Q07 | Q07 | kit1Led8 |
| Kit2 Botão 1 | `altus/kit2/pushbutton/1` | CMD_Q08 | Q08 | kit2Led1 |
| Kit2 Botão 2 | `altus/kit2/pushbutton/2` | CMD_Q09 | Q09 | kit2Led2 |
| Kit2 Botão 3 | `altus/kit2/pushbutton/3` | CMD_Q10 | Q10 | kit2Led3 |
| Kit2 Botão 4 | `altus/kit2/pushbutton/4` | CMD_Q11 | Q11 | kit2Led4 |
| Kit2 Switch 1 | `altus/kit2/switch/1` | CMD_Q12 | Q12 | kit2Led5 |
| Kit2 Switch 2 | `altus/kit2/switch/2` | CMD_Q13 | Q13 | kit2Led6 |
| Kit2 Switch 3 | `altus/kit2/switch/3` | CMD_Q14 | Q14 | kit2Led7 |
| Kit2 Switch 4 | `altus/kit2/switch/4` | CMD_Q15 | Q15 | kit2Led8 |
