plugins {
    kotlin("jvm") version "1.9.22"
    kotlin("plugin.serialization") version "1.9.22"
    id("io.ktor.plugin") version "2.3.8"
}

group = "com.altus"
version = "0.0.1"

application {
    mainClass.set("com.altus.gateway.ApplicationKt")
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("io.ktor:ktor-server-core-jvm:2.3.8")
    implementation("io.ktor:ktor-server-netty-jvm:2.3.8")
    implementation("io.ktor:ktor-server-websockets-jvm:2.3.8")
    implementation("io.ktor:ktor-server-cors-jvm:2.3.8")
    implementation("io.ktor:ktor-serialization-kotlinx-json-jvm:2.3.8")
    implementation("io.ktor:ktor-server-content-negotiation-jvm:2.3.8")
    implementation("ch.qos.logback:logback-classic:1.4.14")
    
    // PLC4X
    implementation("org.apache.plc4x:plc4j-api:0.13.1")
    implementation("org.apache.plc4x:plc4j-driver-eip:0.13.1")
}
