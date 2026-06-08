package com.example.altusmobileapp.ui

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.altusmobileapp.network.GatewayCommand
import com.example.altusmobileapp.network.GatewayHandler
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach
import kotlinx.serialization.json.Json

class MainViewModel : ViewModel() {
    private val gatewayHandler = GatewayHandler(viewModelScope)

    var onStatusUpdateReceived: ((topic: String, status: String) -> Unit)? = null

    private val jsonParser = Json { ignoreUnknownKeys = true }

    init {
        gatewayHandler.messages.onEach { message ->
            try {
                val update = jsonParser.decodeFromString<GatewayCommand>(message)
                if (update.action == "update") {
                    onStatusUpdateReceived?.invoke(update.tag, update.value)
                }
            } catch (e: Exception) {
                Log.e("MainViewModel", "Failed to parse websocket message: $message", e)
            }
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
