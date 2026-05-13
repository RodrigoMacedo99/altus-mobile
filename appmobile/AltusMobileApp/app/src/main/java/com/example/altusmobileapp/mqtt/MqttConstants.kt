package com.example.altusmobileapp.mqtt

object MqttConstants {
    const val BROKER_URL = "mqtt-dashboard.com"
    const val BROKER_PORT = 8883

    // Estrutura base
    private const val BASE = "altus"

    // Tipos de componentes
    const val TYPE_PUSHBUTTON = "pushbutton"
    const val TYPE_SWITCH = "switch"


    // Exemplo de resultado: "altus/kit1/pushbutton/1"
    fun getTopic(kit: Int, tipo: String, id: Int): String {
        return "$BASE/kit$kit/$tipo/$id"
    }

    // Para ouvir TUDO o que acontece nos kits
    const val SUBSCRIBE_ALL_KITS = "$BASE/#"

    const val PAYLOAD_ON = "1"
    const val PAYLOAD_OFF = "0"
}