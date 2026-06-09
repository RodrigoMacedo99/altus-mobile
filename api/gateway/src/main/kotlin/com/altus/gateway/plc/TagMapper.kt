package com.altus.gateway.plc

object TagMapper {

    private val tagMap = mapOf(
        "altus/kit1/pushbutton/1" to "%IX0.0:BOOL",
        "altus/kit1/pushbutton/2" to "%IX0.1:BOOL",
        "altus/kit1/pushbutton/3" to "%IX0.2:BOOL",
        "altus/kit1/pushbutton/4" to "%IX0.3:BOOL",
        
        "altus/kit1/switch/1" to "%IX0.4:BOOL",
        "altus/kit1/switch/2" to "%IX0.5:BOOL",
        "altus/kit1/switch/3" to "%IX0.6:BOOL",
        "altus/kit1/switch/4" to "%IX0.7:BOOL",
        
        "altus/kit1/led/1" to "%QX0.0:BOOL",
        "altus/kit1/led/2" to "%QX0.1:BOOL",
        "altus/kit1/led/3" to "%QX0.2:BOOL",
        "altus/kit1/led/4" to "%QX0.3:BOOL",
        "altus/kit1/led/5" to "%QX0.4:BOOL",
        "altus/kit1/led/6" to "%QX0.5:BOOL",
        "altus/kit1/led/7" to "%QX0.6:BOOL",
        "altus/kit1/led/8" to "%QX0.7:BOOL",
    )

    fun toPlcTag(mobileTag: String): String? {
        if (mobileTag.contains("kit2")) {
            return null
        }
        return tagMap[mobileTag]
    }
    
    fun getMobileTagsToPoll(): List<String> {
        return tagMap.keys.toList()
    }
}
