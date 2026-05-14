import java.util.Properties

plugins {
    alias(libs.plugins.android.application)
}

val localProperties = Properties()
val localPropertiesFile = rootProject.file("local.properties")
if (localPropertiesFile.exists()) {
    localProperties.load(localPropertiesFile.inputStream())
}

// Função auxiliar para limpar as strings do local.properties
fun getMqttProperty(key: String, default: String = ""): String {
    val value = localProperties.getProperty(key) ?: default
    return if (value == "null") "" else value
}

android {
    namespace = "com.example.altusmobileapp"
    compileSdk {
        version = release(36) {
            minorApiLevel = 1
        }
    }

    defaultConfig {
        applicationId = "com.example.altusmobileapp"
        minSdk = 24
        targetSdk = 36
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"

        // Injetando as variáveis de forma segura
        buildConfigField("String", "MQTT_USER", "\"${getMqttProperty("mqtt.user")}\"")
        buildConfigField("String", "MQTT_PASSWORD", "\"${getMqttProperty("mqtt.password")}\"")
        buildConfigField("String", "BROKER_URL", "\"${getMqttProperty("mqtt.url", "broker.hivemq.com")}\"")
        buildConfigField("int", "BROKER_PORT", getMqttProperty("mqtt.port", "1883"))
        buildConfigField("boolean", "USE_SSL", getMqttProperty("mqtt.use_ssl", "false"))
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    buildFeatures {
        buildConfig = true
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }

    packaging {
        resources {
            excludes += "META-INF/INDEX.LIST"
            excludes += "META-INF/io.netty.versions.properties"
        }
    }
}

dependencies {
    implementation(libs.androidx.activity.ktx)
    implementation(libs.androidx.appcompat)
    implementation(libs.androidx.constraintlayout)
    implementation(libs.androidx.core.ktx)
    implementation(libs.material)
    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.espresso.core)
    androidTestImplementation(libs.androidx.junit)
    implementation(libs.hivemq.mqtt.client)
}
