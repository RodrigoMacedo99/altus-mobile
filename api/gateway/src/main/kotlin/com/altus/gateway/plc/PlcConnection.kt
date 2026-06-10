package com.altus.gateway.plc

import org.apache.plc4x.java.api.PlcConnection as Plc4xConnection
import org.apache.plc4x.java.api.PlcDriverManager
import org.slf4j.LoggerFactory

class PlcConnection {
    private val logger = LoggerFactory.getLogger(PlcConnection::class.java)
    private val isMock = System.getenv("MOCK_PLC")?.toBoolean() ?: true
    private val clpIp = System.getenv("CLP_IP") ?: "192.168.0.100"
    private val slot = System.getenv("CLP_SLOT") ?: "0"

    private var connection: Plc4xConnection? = null
    
    // Armazena os valores no mock mode
    private val mockValues = mutableMapOf<String, String>()

    init {
        if (!isMock) {
            connect()
        } else {
            logger.info("Starting PlcConnection in MOCK mode. No real connection to CLP will be established.")
        }
    }

    private fun connect() {
        try {
            val connectionString = "eip://$clpIp:44818?backplane=1&slot=$slot&force-unconnected-operation=true"
            logger.info("Connecting to PLC via: $connectionString")
            connection = PlcDriverManager.getDefault().connectionManager.getConnection(connectionString)
            logger.info("Connected to PLC successfully.")
        } catch (e: Exception) {
            logger.error("Failed to connect to PLC", e)
        }
    }

    fun writeTag(mobileTag: String, value: String) {
        val plcTag = TagMapper.toPlcTag(mobileTag)
        if (plcTag == null) {
            logger.warn("Ignoring write for unknown or ignored tag: $mobileTag")
            return
        }

        if (isMock) {
            logger.info("[MOCK] Writing to $plcTag ($mobileTag) value: $value")
            mockValues[mobileTag] = value
            return
        }

        try {
            val conn = connection ?: return
            if (!conn.isConnected) connect()
            
            val booleanValue = value == "1" || value.equals("true", ignoreCase = true)
            
            val writeRequest = conn.writeRequestBuilder()
                .addTagAddress(mobileTag, plcTag, booleanValue)
                .build()
                
            writeRequest.execute().get()
            logger.info("Wrote to PLC: $plcTag = $booleanValue")
        } catch (e: Exception) {
            logger.error("Failed to write to PLC tag $plcTag", e)
        }
    }

    fun pollTags(): Map<String, String> {
        val results = mutableMapOf<String, String>()
        val tagsToPoll = TagMapper.getMobileTagsToPoll()
        
        if (isMock) {
            tagsToPoll.forEach { tag ->
                results[tag] = mockValues[tag] ?: "0"
            }
            return results
        }

        try {
            val conn = connection ?: return results
            if (!conn.isConnected) connect()

            val readRequestBuilder = conn.readRequestBuilder()
            tagsToPoll.forEach { mobileTag ->
                val plcTag = TagMapper.toPlcTag(mobileTag)
                if (plcTag != null) {
                    readRequestBuilder.addTagAddress(mobileTag, plcTag)
                }
            }
            
            val readRequest = readRequestBuilder.build()
            val response = readRequest.execute().get()
            
            tagsToPoll.forEach { mobileTag ->
                try {
                    val value = response.getBoolean(mobileTag)
                    results[mobileTag] = if (value) "1" else "0"
                } catch (e: Exception) {
                    // Ignore missing or errored reads in batch
                }
            }
        } catch (e: Exception) {
            logger.error("Failed to read from PLC", e)
        }
        
        return results
    }
}
