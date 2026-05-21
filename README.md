# Redes Industriais - Altus Mobile

Este projeto é um aplicativo móvel desenvolvido para interagir com kits de automação da Altus através de uma arquitetura de comunicação IoT/Industrial.

## Arquitetura do Sistema

A arquitetura de comunicação do projeto funciona da seguinte maneira:

1. **Aplicativo Mobile:** O aplicativo atua como a interface do usuário e se comunica através do protocolo **MQTT**.
2. **Broker MQTT:** Um broker MQTT rodando em um computador intermediário recebe as mensagens do aplicativo móvel e as encaminha para a rede industrial.
3. **Kit Altus (Master):** O kit de automação Master está conectado ao broker e atua como o nó central de comunicação na rede física.
4. **Kit Altus (Slave):** O kit Slave está conectado ao kit Master através de uma rede serial utilizando o protocolo **Modbus RTU**.

### Fluxo de Comunicação

Toda a interação do aplicativo móvel com a planta (seja monitoramento ou controle) é feita através do MQTT. A mensagem sai do Mobile, passa pelo Broker e chega ao Kit Master. 

Caso o destino da interação seja o Kit Slave, o Kit Master é responsável por repassar a informação recebida via MQTT e enviar os comandos correspondentes utilizando **Modbus RTU**. Sendo assim, a comunicação do Mobile com o Kit Slave **sempre** passa pelo Kit Master, que atua como uma ponte/gateway entre a rede MQTT e a rede Modbus RTU.
