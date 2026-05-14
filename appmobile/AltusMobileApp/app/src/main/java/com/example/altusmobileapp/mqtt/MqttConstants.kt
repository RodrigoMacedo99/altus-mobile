package com.example.altusmobileapp.mqtt

import com.example.altusmobileapp.BuildConfig

object MqttConstants {
    val BROKER_URL = BuildConfig.BROKER_URL
    val BROKER_PORT = BuildConfig.BROKER_PORT
    val USE_SSL = BuildConfig.USE_SSL
    val MQTT_USER = BuildConfig.MQTT_USER
    val MQTT_PASSWORD = BuildConfig.MQTT_PASSWORD

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