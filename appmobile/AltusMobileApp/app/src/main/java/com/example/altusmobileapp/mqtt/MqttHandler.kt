package com.example.altusmobileapp.mqtt

import android.util.Log
import com.hivemq.client.mqtt.mqtt5.Mqtt5AsyncClient
import com.hivemq.client.mqtt.mqtt5.Mqtt5Client
import java.util.UUID

class MqttHandler {

    private var client: Mqtt5AsyncClient? = null

    /**
     * Conecta ao broker e inicia a escuta global de todos os kits.
     */
    fun connect(onMessageReceived: (topic: String, message: String) -> Unit) {
        client = Mqtt5Client.builder()
            .identifier("altus_mobile_${UUID.randomUUID()}") // ID único
            .serverHost(MqttConstants.BROKER_URL)
            .serverPort(MqttConstants.BROKER_PORT)
            .sslWithDefaultConfig()
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
        val isConnected = client?.state?.isConnected ?: false

        if (!isConnected) {
            Log.e("MQTT", "Can't publish on $topic: Client disconnected. Trying to reconnect...")
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