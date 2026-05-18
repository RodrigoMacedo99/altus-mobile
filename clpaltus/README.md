# CLP Altus XP340 — Configuração MQTT

## Fluxo de comunicação

```
App Android (celular)
        |
        | MQTT (publica tópico)
        v
  Mosquitto (broker)
  192.168.X.X : 1883
        |
        | MQTT (entrega ao subscriber)
        v
  CLP XP340
  (assina os tópicos e atua nas saídas)
```

## Configuração MQTT no XP340 (MasterTool IEC XE)

No MasterTool, configure o bloco de comunicação MQTT com os parâmetros abaixo:

| Parâmetro        | Valor                         |
|------------------|-------------------------------|
| Broker Host      | IP do PC com Mosquitto        |
| Broker Port      | 1883                          |
| Client ID        | `clp_xp340_kit1` (único)      |
| Username         | *(vazio se allow_anonymous)*  |
| Password         | *(vazio se allow_anonymous)*  |
| Keep Alive       | 60 s                          |
| Clean Session    | true                          |

## Tópicos MQTT

### Estrutura

```
altus / kit{N} / {tipo} / {id}
```

- `{N}` = número do kit (1 ou 2)
- `{tipo}` = `pushbutton` ou `switch`
- `{id}` = número do componente (1 a 4)

### O CLP deve **assinar (subscribe)** estes tópicos

O app publica nesses tópicos quando o usuário interage com a tela.

| Tópico                      | Payload | Significado                        |
|-----------------------------|---------|------------------------------------|
| `altus/kit1/pushbutton/1`   | `1`     | Botão 1 do Kit 1 pressionado       |
| `altus/kit1/pushbutton/1`   | `0`     | Botão 1 do Kit 1 solto             |
| `altus/kit1/pushbutton/2`   | `1`/`0` | Botão 2 do Kit 1                   |
| `altus/kit1/pushbutton/3`   | `1`/`0` | Botão 3 do Kit 1                   |
| `altus/kit1/pushbutton/4`   | `1`/`0` | Botão 4 do Kit 1                   |
| `altus/kit1/switch/1`       | `1`     | Switch 1 do Kit 1 ligado           |
| `altus/kit1/switch/1`       | `0`     | Switch 1 do Kit 1 desligado        |
| `altus/kit1/switch/2`       | `1`/`0` | Switch 2 do Kit 1                  |
| `altus/kit1/switch/3`       | `1`/`0` | Switch 3 do Kit 1                  |
| `altus/kit1/switch/4`       | `1`/`0` | Switch 4 do Kit 1                  |
| `altus/kit2/pushbutton/1-4` | `1`/`0` | Botões 1-4 do Kit 2 (mesmo padrão) |
| `altus/kit2/switch/1-4`     | `1`/`0` | Switches 1-4 do Kit 2              |

Para assinar todos de uma vez: **`altus/#`**

### O CLP pode **publicar (publish)** de volta (opcional)

Se o CLP publicar nos mesmos tópicos, os LEDs do app são atualizados com o estado real da saída.

| Tópico                    | Payload | Significado               |
|---------------------------|---------|---------------------------|
| `altus/kit1/pushbutton/1` | `1`     | Saída ativa (LED verde)   |
| `altus/kit1/pushbutton/1` | `0`     | Saída inativa (LED cinza) |

## Mapeamento LED ↔ Tópico no App

| LED no app  | Tópico MQTT               |
|-------------|---------------------------|
| Kit1 LED 1  | `altus/kit1/pushbutton/1` |
| Kit1 LED 2  | `altus/kit1/pushbutton/2` |
| Kit1 LED 3  | `altus/kit1/pushbutton/3` |
| Kit1 LED 4  | `altus/kit1/pushbutton/4` |
| Kit1 LED 5  | `altus/kit1/switch/1`     |
| Kit1 LED 6  | `altus/kit1/switch/2`     |
| Kit1 LED 7  | `altus/kit1/switch/3`     |
| Kit1 LED 8  | `altus/kit1/switch/4`     |
| Kit2 LED 1  | `altus/kit2/pushbutton/1` |
| Kit2 LED 2  | `altus/kit2/pushbutton/2` |
| Kit2 LED 3  | `altus/kit2/pushbutton/3` |
| Kit2 LED 4  | `altus/kit2/pushbutton/4` |
| Kit2 LED 5  | `altus/kit2/switch/1`     |
| Kit2 LED 6  | `altus/kit2/switch/2`     |
| Kit2 LED 7  | `altus/kit2/switch/3`     |
| Kit2 LED 8  | `altus/kit2/switch/4`     |

## Passos para colocar em funcionamento

1. **PC Windows (Mosquitto)**
   - Copie `infra/mosquitto/mosquitto.conf` para `C:\Program Files\mosquitto\`
   - Crie as pastas: `C:\mosquitto\data\` e `C:\mosquitto\log\`
   - Inicie o serviço: `net start mosquitto`
   - Verifique o IP do PC: `ipconfig` (anote o "Endereço IPv4")

2. **App Android**
   - No projeto, copie `local.properties.example` → `local.properties`
   - Preencha `mqtt.url` com o IP do PC onde o Mosquitto está rodando
   - Rebuild e instale no celular

3. **CLP XP340**
   - No MasterTool, configure o cliente MQTT com o IP e porta do Mosquitto
   - Adicione subscriptions para os tópicos `altus/#` (ou tópico a tópico)
   - Mapeie cada tópico recebido para a variável/saída correspondente no programa ladder

4. **Teste**
   - Use o `mosquitto_sub` no PC para monitorar: `mosquitto_sub -h localhost -t "altus/#" -v`
   - Pressione um botão no app e verifique se a mensagem aparece no terminal
   - Confirme que o CLP recebe e atua na saída correspondente
