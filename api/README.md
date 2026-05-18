# Altus MQTT Broker

## Visão geral

Este diretório contém a infraestrutura do Broker MQTT (Eclipse Mosquitto) responsável por intermediar a comunicação entre o aplicativo móvel (App Mobile) e o Kit de Automação Altus (Kit 1).

A topologia é a seguinte:

1. **App Mobile** <-> **Broker MQTT (Computador)** via rede (Wi-Fi/Internet).
2. **Broker MQTT (Computador)** <-> **Kit 1 (CLP Altus)** via rede.
3. **Kit 1** <-> **Kit 2** via rede Modbus RTU (cabo serial). O Kit 1 age como Mestre na rede serial para repassar ou espelhar os comandos para o Kit 2.

## Arquitetura e componentes

A arquitetura baseia-se unicamente em um container Docker:

- `docker-compose.yml`: Arquivo de orquestração do Docker, define o serviço `mosquitto` rodando na porta padrão MQTT `1883`.
- `broker/mosquitto.conf`: Arquivo de configuração do Eclipse Mosquitto. Você pode adicionar regras de portas, autenticação e websockets aqui se necessário.
- `broker/passwords.txt`: Arquivo que armazena a lista de usuários e senhas para autenticar os clientes MQTT (Mobile e Kit 1).

## Execução (Deploy Local)

Para iniciar o broker no seu computador:

1. Instale o Docker e o Docker Compose.
2. Navegue até a pasta onde este `README.md` se encontra.
3. Execute o comando:
   ```bash
   docker compose up -d
   ```
4. O broker estará rodando e aceitando conexões MQTT na porta **1883**.

## Padrão de Tópicos

Para o funcionamento correto sem nenhum tipo de backend intermediário (como a antiga API de tradução), é imperativo que o **App Mobile** e o **CLP Altus** sejam configurados para assinar (Subscribe) e publicar (Publish) nos mesmos tópicos e com o mesmo formato de mensagens (Payload).

**Exemplo Recomendado de Tópicos:**

- `altus/kit1/pushbutton/1` -> Estado do botão 1 do Kit 1.
- `altus/kit1/switch/1` -> Estado do switch 1 do Kit 1.

## Dicas Úteis / Troubleshooting

- Para ler todos os tópicos passando pelo broker no terminal:
  ```bash
  mosquitto_sub -h localhost -t "#" -v
  ```
- Para testar publicar uma mensagem ligando um componente:
  ```bash
  mosquitto_pub -h localhost -t "altus/kit1/pushbutton/1" -m "1" -r
  ```
- Se o App Mobile e o Kit 1 estiverem na mesma rede, eles devem usar o IP local (ex: `192.168.1.x`) do computador host executando o Docker como endereço do Broker.
