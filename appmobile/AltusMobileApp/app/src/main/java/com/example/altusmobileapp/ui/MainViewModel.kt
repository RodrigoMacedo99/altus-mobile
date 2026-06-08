package com.example.altusmobileapp.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.altusmobileapp.network.GatewayHandler
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach

class MainViewModel : ViewModel() {
    private val gatewayHandler = GatewayHandler(viewModelScope)

    var onStatusUpdateReceived: ((topic: String, status: String) -> Unit)? = null

    init {
        gatewayHandler.messages.onEach { message ->
            // Aqui você pode parsear o JSON de resposta do seu backend
            // e chamar o callback de atualização da UI
            onStatusUpdateReceived?.invoke("gateway", message)
        }.launchIn(viewModelScope)
        
        gatewayHandler.connect()
    }

    fun sendPushButtonCommand(kit: Int, id: Int, isPressed: Boolean) {
        val value = if (isPressed) "1" else "0"
        gatewayHandler.sendCommand(kit, "pushbutton", id, value)
    }

    fun sendSwitchCommand(kit: Int, id: Int, isOn: Boolean) {
        val value = if (isOn) "1" else "0"
        gatewayHandler.sendCommand(kit, "switch", id, value)
    }

    override fun onCleared() {
        super.onCleared()
        gatewayHandler.disconnect()
    }
}
