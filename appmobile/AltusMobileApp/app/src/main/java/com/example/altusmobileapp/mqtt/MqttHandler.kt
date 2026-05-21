package com.example.altusmobileapp.mqtt

import android.util.Log
import com.hivemq.client.mqtt.mqtt5.Mqtt5AsyncClient
import com.hivemq.client.mqtt.mqtt5.Mqtt5Client
import java.util.UUID

class MqttHandler {

    private var client: Mqtt5AsyncClient? = null
    private var messageCallback: ((String, String) -> Unit)? = null

    /**
     * Conecta ao broker e inicia a escuta global de todos os kits.
     */
    fun connect(onMessageReceived: (topic: String, message: String) -> Unit) {
        this.messageCallback = onMessageReceived
        var builder = Mqtt5Client.builder()
            .identifier("altus_mobile_${UUID.randomUUID()}")
            .serverHost(MqttConstants.BROKER_URL)
            .serverPort(MqttConstants.BROKER_PORT)

        // Aplica SSL apenas se configurado
        if (MqttConstants.USE_SSL) {
            builder = builder.sslWithDefaultConfig()
        }

        // Aplica autenticação apenas se usuário e senha existirem
        if (MqttConstants.MQTT_USER.isNotEmpty() && MqttConstants.MQTT_PASSWORD.isNotEmpty()) {
            builder = builder.simpleAuth()
                .username(MqttConstants.MQTT_USER)
                .password(MqttConstants.MQTT_PASSWORD.toByteArray())
                .applySimpleAuth()
        }

        client = builder
            .automaticReconnectWithDefaultConfig()
            .buildAsync()

        client?.connect()?.whenComplete { _, throwable ->
            if (throwable != null) {
                Log.e("MQTT", "Connection failed: ${throwable.message}")
                android.os.Handler(android.os.Looper.getMainLooper()).postDelayed({
                    connect(onMessageReceived)
                }, 5000)
            } else {
                Log.d("MQTT", "Connected to Broker: ${MqttConstants.BROKER_URL}")
                subscribeToAll(onMessageReceived)
            }
        }
    }

    /**
     * Se inscreve no tópico global usando o coringa '#'
     */
    private fun subscribeToAll(onMessageReceived: (String, String) -> Unit) {
        client?.subscribeWith()
            ?.topicFilter(MqttConstants.SUBSCRIBE_ALL_KITS) // "altus/#"
            ?.callback { publish ->
                val message = String(publish.payloadAsBytes)
                val topic = publish.topic.toString()

                Log.d("MQTT", "Received -> $topic: $message")
                android.os.Handler(android.os.Looper.getMainLooper()).post {
                    onMessageReceived(topic, message)
                }
            }
            ?.send()
    }

    /**
     * Envia uma mensagem (Publica) em um tópico
     */
    fun publish(topic: String, message: String) {
        val state = client?.state
        val isConnected = state?.isConnected ?: false

        if (!isConnected) {
            Log.e("MQTT", "Can't publish on $topic: Client is ${state?.name ?: "NULL"}. Trying to reconnect...")
            // Se estiver desconectado (não apenas conectando), tenta reconectar
            if (state?.name == "DISCONNECTED" || state == null) {
                messageCallback?.let { connect(it) }
            }
            return
        }

        client?.publishWith()
            ?.topic(topic)
            ?.payload(message.toByteArray())
            ?.send()
            ?.whenComplete { _, throwable ->
                if (throwable != null) {
                    Log.e("MQTT", "Error to publish on $topic: ${throwable.message}")
                }
            }
    }

    fun disconnect() {
        client?.disconnect()
    }
}