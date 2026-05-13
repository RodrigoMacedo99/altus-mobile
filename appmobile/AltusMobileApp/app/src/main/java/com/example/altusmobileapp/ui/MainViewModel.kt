package com.example.altusmobileapp.ui

import androidx.lifecycle.ViewModel
import com.example.altusmobileapp.mqtt.MqttConstants
import com.example.altusmobileapp.mqtt.MqttHandler

class MainViewModel : ViewModel() {
    private val mqttHandler = MqttHandler()

    var onStatusUpdateReceived: ((topic: String, status: String) -> Unit)? = null

    init {
        mqttHandler.connect { topic, message ->
            onStatusUpdateReceived?.invoke(topic, message)
        }
    }

    fun sendPushButtonCommand(kit: Int, id: Int, isPressed: Boolean) {
        val topic = MqttConstants.getTopic(kit, MqttConstants.TYPE_PUSHBUTTON, id)
        val payload = if (isPressed) MqttConstants.PAYLOAD_ON else MqttConstants.PAYLOAD_OFF
        mqttHandler.publish(topic, payload)
    }

    fun sendSwitchCommand(kit: Int, id: Int, isOn: Boolean) {
        val topic = MqttConstants.getTopic(kit, MqttConstants.TYPE_SWITCH, id)
        val payload = if (isOn) MqttConstants.PAYLOAD_ON else MqttConstants.PAYLOAD_OFF
        mqttHandler.publish(topic, payload)
    }

    override fun onCleared() {
        super.onCleared()
        mqttHandler.disconnect()
    }
}