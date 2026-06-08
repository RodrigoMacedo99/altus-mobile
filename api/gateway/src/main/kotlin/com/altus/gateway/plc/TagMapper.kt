package com.altus.gateway.plc

object TagMapper {

    // Simulação do mapeamento de tags para nomes simbólicos no CLP MasterTool
    // A SER PREENCHIDO COM OS NOMES REAIS EXPORTADOS DO MASTERTOOL
    private val tagMap = mapOf(
        "altus/kit1/pushbutton/1" to "%{Kit1_PB1}:BOOL",
        "altus/kit1/pushbutton/2" to "%{Kit1_PB2}:BOOL",
        "altus/kit1/pushbutton/3" to "%{Kit1_PB3}:BOOL",
        "altus/kit1/pushbutton/4" to "%{Kit1_PB4}:BOOL",
        
        "altus/kit1/switch/1" to "%{Kit1_SW1}:BOOL",
        "altus/kit1/switch/2" to "%{Kit1_SW2}:BOOL",
        "altus/kit1/switch/3" to "%{Kit1_SW3}:BOOL",
        "altus/kit1/switch/4" to "%{Kit1_SW4}:BOOL"
    )

    fun toPlcTag(mobileTag: String): String? {
        if (mobileTag.contains("kit2")) {
            // Ignora kit 2 conforme combinado
            return null
        }
        return tagMap[mobileTag]
    }
    
    fun getMobileTagsToPoll(): List<String> {
        return tagMap.keys.toList()
    }
}
