package com.example.altusmobileapp.network

import android.util.Log
import com.example.altusmobileapp.BuildConfig
import io.ktor.client.*
import io.ktor.client.plugins.websocket.*
import io.ktor.serialization.kotlinx.*
import io.ktor.websocket.*
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*
import kotlinx.serialization.Serializable
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json

@Serializable
data class GatewayCommand(
    val action: String,
    val tag: String,
    val value: String
)

class GatewayHandler(private val scope: CoroutineScope) {

    private val client = HttpClient {
        install(WebSockets) {
            contentConverter = KotlinxWebsocketSerializationConverter(Json)
        }
    }

    private var session: DefaultClientWebSocketSession? = null
    
    private val _messages = MutableSharedFlow<String>()
    val messages = _messages.asSharedFlow()

    private val _isConnected = MutableStateFlow(false)
    val isConnected = _isConnected.asStateFlow()

    fun connect() {
        scope.launch {
            while (isActive) {
                try {
                    Log.d("Gateway", "Connecting to ${BuildConfig.GATEWAY_URL}...")
                    client.webSocket(BuildConfig.GATEWAY_URL) {
                        session = this
                        _isConnected.value = true
                        Log.d("Gateway", "Connected!")
                        
                        for (frame in incoming) {
                            if (frame is Frame.Text) {
                                val text = frame.readText()
                                Log.d("Gateway", "Received: $text")
                                _messages.emit(text)
                            }
                        }
                    }
                } catch (e: Exception) {
                    Log.e("Gateway", "Connection error: ${e.message}")
                } finally {
                    session = null
                    _isConnected.value = false
                    Log.d("Gateway", "Disconnected. Retrying in 5s...")
                    delay(5000)
                }
            }
        }
    }

    fun sendCommand(kit: Int, type: String, id: Int, value: String) {
        val tag = "altus/kit$kit/$type/$id"
        val command = GatewayCommand(action = "write", tag = tag, value = value)
        val jsonCommand = Json.encodeToString(command)
        
        scope.launch {
            try {
                session?.send(Frame.Text(jsonCommand))
                Log.d("Gateway", "Sent: $jsonCommand")
            } catch (e: Exception) {
                Log.e("Gateway", "Error sending command: ${e.message}")
            }
        }
    }

    fun disconnect() {
        scope.launch {
            session?.close()
            client.close()
        }
    }
}
