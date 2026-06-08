package com.altus.gateway.model

import kotlinx.serialization.Serializable

@Serializable
data class GatewayCommand(
    val action: String,
    val tag: String,
    val value: String
)


