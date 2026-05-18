# Guia: Conectar o CLP XP340 com o Broker Mosquitto

Os arquivos de código prontos estão na pasta `clpaltus/codigo/`.
Você vai copiar o conteúdo deles para dentro do MasterTool.

---

## Antes de começar

Você vai precisar de:
- MasterTool aberto com seu projeto do CLP
- Mosquitto instalado no PC (pasta `C:\Program Files\mosquitto`)
- CLP XP340 conectado ao PC via rede

---

## PARTE 1 — Configurar o MasterTool

### Passo 1 — Adicionar a biblioteca LibMQTT

> Sem esta biblioteca, nenhum dos programas abaixo vai funcionar.

1. No painel **Devices** (lado esquerdo), clique duas vezes em **Library Manager**
2. Clique no botão **"Add Library"** (canto superior esquerdo da janela)
3. Na caixinha de busca que aparecer, **digite:** `mqtt`
4. Clique em **LibMQTT** (vai aparecer com fundo amarelo na lista)
5. Clique **OK**

Agora ajuste os parâmetros da biblioteca:

6. Na lista de bibliotecas, clique em **LibMQTT** para selecionar
7. No painel inferior direito, clique na aba **"Library Parameters"**
8. Clique no campo do valor de **gc_uMaxSubs** e **digite:** `50`
9. Clique no campo do valor de **gc_uMaxPubs** e **digite:** `50`

---

### Passo 2 — Criar a pasta MQTT no projeto

1. No painel **Devices**, clique com o **botão direito** em **Application**
2. Clique em **Add Object** → **Folder**
3. **Digite o nome:** `MQTT`
4. Clique **OK**

---

### Passo 3 — Criar a GVL_MQTT

1. Clique com o **botão direito** na pasta **MQTT** que acabou de criar
2. Clique em **Add Object** → **Global Variable List**
3. **Digite o nome:** `GVL_MQTT`
4. Clique **OK**

A GVL vai abrir em branco. Agora:

5. Abra o arquivo `clpaltus/codigo/GVL_MQTT.st` no Bloco de Notas
6. Pressione **Ctrl+A** para selecionar tudo
7. Pressione **Ctrl+C** para copiar
8. Volte ao MasterTool, clique dentro da área de texto da GVL
9. Selecione todo o texto que já existe com **Ctrl+A**
10. Cole com **Ctrl+V**
11. Salve com **Ctrl+S**

---

### Passo 4 — Criar o programa ESPELHAMENTO_SAIDAS_MQTT

1. Clique com o **botão direito** na pasta **MQTT**
2. Clique em **Add Object** → **POU**
3. **Nome:** `ESPELHAMENTO_SAIDAS_MQTT`
4. Em "Type", marque **Program**
5. Em "Implementation language", selecione **Structured Text (ST)**
6. Clique **OK**

O editor vai abrir. Agora:

7. Abra o arquivo `clpaltus/codigo/ESPELHAMENTO_SAIDAS_MQTT.st` no Bloco de Notas
8. Copie tudo (**Ctrl+A** → **Ctrl+C**)
9. No MasterTool, clique na área de código (parte de baixo do editor)
10. Selecione tudo (**Ctrl+A**) e cole (**Ctrl+V**)
11. Salve com **Ctrl+S**

---

### Passo 5 — Criar o programa MQTT

1. Clique com o **botão direito** na pasta **MQTT**
2. Clique em **Add Object** → **POU**
3. **Nome:** `MQTT`
4. Em "Type", marque **Program**
5. Em "Implementation language", selecione **Structured Text (ST)**
6. Clique **OK**

O editor vai abrir com duas áreas: **VAR** (em cima) e **código** (em baixo).

7. Abra o arquivo `clpaltus/codigo/MQTT.st` no Bloco de Notas

**Na área VAR (parte de cima do editor no MasterTool):**

8. Apague o conteúdo que já existe com **Ctrl+A** → **Delete**
9. Cole este trecho:

```
VAR
    MQTT_FB            : MQTT_CLIENT;
    MQTT_FB_Enable     : BOOL := TRUE;
    MQTT_FB_Error      : BOOL;
    MQTT_FB_State      : MQTT_STATES;
    MQTT_FB_Error_Code : MQTT_ERR_CODE;
    i                  : INT;
END_VAR
```

**Na área de código (parte de baixo do editor):**

10. Apague o conteúdo com **Ctrl+A** → **Delete**
11. Cole o restante do arquivo `MQTT.st` (a parte depois do comentário `===== CÓDIGO =====`)

**IMPORTANTE — troque o IP:**

12. No código colado, localize a linha:
    ```
    MQTT_FB_CONNECTION_CONFIG.sHostname := '192.168.X.X';
    ```
13. Troque `192.168.X.X` pelo IP real do seu PC (veja como descobrir abaixo)
14. Salve com **Ctrl+S**

---

### Passo 6 — Descobrir o IP do seu PC

1. Pressione **Windows + R**, digite `cmd` e pressione Enter
2. No CMD que abrir, **digite:** `ipconfig` e pressione Enter
3. Procure pela linha **"Endereço IPv4"** (algo como `192.168.1.100`)
4. Esse é o IP que você deve colocar no `sHostname`

---

### Passo 7 — Adicionar os programas na Task

1. No painel **Devices**, expanda **Task Configuration** → **MainTask**
2. Clique com o **botão direito** em **MainTask** → **"Add Call"**
3. Selecione **ESPELHAMENTO_SAIDAS_MQTT** → OK
4. Repita e selecione **MQTT** → OK

---

### Passo 8 — Carregar no CLP

1. Pressione **F11** para compilar (Build)
2. Se aparecer "0 errors", pressione **F8** para conectar ao CLP (Login)
3. Confirme o download clicando em **Yes**
4. Pressione **F5** para iniciar a execução

---

## PARTE 2 — Configurar o Mosquitto no PC

### Passo 9 — Copiar o arquivo de configuração

O arquivo de configuração já está pronto no projeto em `infra/mosquitto/mosquitto.conf`.

1. Abra o **Explorador de Arquivos**
2. Navegue até `C:\Sistemas\Faculdade\altus-mobile\infra\mosquitto\`
3. Copie o arquivo `mosquitto.conf`
4. Cole em `C:\Program Files\mosquitto\` (substitua se pedir)

Agora crie as pastas que o Mosquitto precisa:

5. Pressione **Windows + R**, digite `cmd` e Enter
6. No CMD, **digite e pressione Enter em cada linha:**
   ```
   mkdir C:\mosquitto\data
   mkdir C:\mosquitto\log
   ```

---

### Passo 10 — Iniciar o Mosquitto

1. Abra o **Explorador de Arquivos** e navegue até `C:\Program Files\mosquitto`
2. Clique na **barra de endereço** (onde aparece o caminho), **digite** `cmd` e pressione **Enter**
3. No CMD que abrir, **digite:**
   ```
   mosquitto -v
   ```
4. Deixe essa janela aberta — ela mostra tudo que está acontecendo

---

## PARTE 3 — Testar a comunicação

### Passo 11 — Verificar se o CLP conectou

Quando o Mosquitto está rodando e o CLP está conectado, na janela do CMD você verá:

```
New connection from 192.168.X.X on port 1883.
New client connected from 192.168.X.X as clp_xp340_kit1
```

### Passo 12 — Testar manualmente pelo CMD

Abra **mais uma janela** de CMD dentro de `C:\Program Files\mosquitto` e teste:

**Enviar "ligar" para a saída Q00 do CLP:**
```
mosquitto_pub -h localhost -p 1883 -t "altus/kit1/pushbutton/1" -m "1"
```

**Enviar "desligar" para a saída Q00:**
```
mosquitto_pub -h localhost -p 1883 -t "altus/kit1/pushbutton/1" -m "0"
```

Se a saída Q00 do CLP ligar/desligar → tudo funcionando!

### Passo 13 — Testar pelo app Android

1. Abra o arquivo `local.properties` no projeto Android
   (se não existir, copie `local.properties.example` e renomeie para `local.properties`)
2. Coloque o IP do seu PC:
   ```
   mqtt.url=192.168.X.X
   ```
3. Instale o app no celular e pressione um botão — a saída do CLP deve responder

---

## Resumo do que cada arquivo faz

| Arquivo | Função |
|---------|--------|
| `GVL_MQTT.st` | Declara as variáveis e lista os tópicos a escutar |
| `ESPELHAMENTO_SAIDAS_MQTT.st` | Mapeia o que chega do app para as saídas Q00-Q07 |
| `MQTT.st` | Conecta ao broker e mantém a comunicação ativa |
| `infra/mosquitto/mosquitto.conf` | Configuração do broker Mosquitto |

## Mapeamento completo App → CLP

| Botão no App | Tópico MQTT | Saída do CLP |
|---|---|---|
| Kit1 Botão 1 | `altus/kit1/pushbutton/1` | Q00 |
| Kit1 Botão 2 | `altus/kit1/pushbutton/2` | Q01 |
| Kit1 Botão 3 | `altus/kit1/pushbutton/3` | Q02 |
| Kit1 Botão 4 | `altus/kit1/pushbutton/4` | Q03 |
| Kit1 Switch 1 | `altus/kit1/switch/1` | Q04 |
| Kit1 Switch 2 | `altus/kit1/switch/2` | Q05 |
| Kit1 Switch 3 | `altus/kit1/switch/3` | Q06 |
| Kit1 Switch 4 | `altus/kit1/switch/4` | Q07 |
