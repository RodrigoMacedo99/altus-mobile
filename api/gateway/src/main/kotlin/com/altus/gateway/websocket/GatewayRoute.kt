package com.altus.gateway.websocket

import com.altus.gateway.model.GatewayCommand
import com.altus.gateway.plc.PlcConnection
import io.ktor.server.application.*
import io.ktor.server.routing.*
import io.ktor.server.websocket.*
import io.ktor.websocket.*
import kotlinx.coroutines.channels.ClosedReceiveChannelException
import kotlinx.coroutines.delay
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import org.slf4j.LoggerFactory
import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.atomic.AtomicInteger

fun Application.configureSockets() {
    val logger = LoggerFactory.getLogger("GatewaySockets")
    val plcConnection = PlcConnection()
    val connections = ConcurrentHashMap<Int, DefaultWebSocketServerSession>()
    val connectionIdCounter = AtomicInteger(0)

    // Polling contínuo (roda apenas 1 vez, independente do número de conexões)
    launch {
        var lastStates = mapOf<String, String>()
        while (isActive) {
            try {
                val currentStates = plcConnection.pollTags()
                val changedStates = currentStates.filter { (tag, value) -> lastStates[tag] != value }
                
                if (changedStates.isNotEmpty()) {
                    lastStates = currentStates
                    
                    changedStates.forEach { (tag, value) ->
                        val update = GatewayCommand(action = "update", tag = tag, value = value)
                        val jsonUpdate = Json.encodeToString(update)
                        
                        // Envia o update para todos os clients conectados
                        connections.values.forEach { session ->
                            try {
                                session.send(Frame.Text(jsonUpdate))
                            } catch (e: Exception) {
                                logger.error("Failed to send update to client", e)
                            }
                        }
                    }
                }
            } catch (e: Exception) {
                logger.error("Error during PLC polling", e)
            }
            delay(200) // Poll a cada 200ms
        }
    }

    routing {
        webSocket("/") {
            val id = connectionIdCounter.getAndIncrement()
            connections[id] = this
            logger.info("Client connected: ID $id")
            
            try {
                for (frame in incoming) {
                    if (frame is Frame.Text) {
                        val text = frame.readText()
                        logger.info("Received from ID $id: $text")
                        
                        try {
                            val command = Json.decodeFromString<GatewayCommand>(text)
                            if (command.action == "write") {
                                plcConnection.writeTag(command.tag, command.value)
                            }
                        } catch (e: Exception) {
                            logger.error("Failed to parse incoming command: $text", e)
                        }
                    }
                }
            } catch (e: ClosedReceiveChannelException) {
                logger.info("Client disconnected: ID $id")
            } catch (e: Exception) {
                logger.error("Error in websocket session ID $id", e)
            } finally {
                connections.remove(id)
            }
        }
    }
}
