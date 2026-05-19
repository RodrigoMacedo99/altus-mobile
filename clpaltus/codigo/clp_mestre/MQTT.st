(*
  ARQUIVO: MQTT.st — CLP MESTRE (gateway)
  ONDE USAR: MasterTool > pasta MQTT > MQTT (PRG)
  O QUE FAZ: mantém a conexão MQTT, assina os 16 tópicos do app
             e publica de volta o retorno do CLP escravo (para atualizar LEDs).

  TROQUE O IP: coloque o IP do PC onde o Mosquitto está rodando.
  Para descobrir: abra o CMD e digite "ipconfig" → "Endereço IPv4"
*)

(* ================================================================
   SEÇÃO VAR — cole na parte de CIMA do editor (área de variáveis)
   ================================================================ *)
(*
VAR
    MQTT_FB            : MQTT_CLIENT;
    MQTT_FB_Enable     : BOOL := TRUE;
    MQTT_FB_Error      : BOOL;
    MQTT_FB_State      : MQTT_STATES;
    MQTT_FB_Error_Code : MQTT_ERR_CODE;
    i                  : INT;
END_VAR
*)

(* ================================================================
   CÓDIGO — cole na parte de BAIXO do editor
   ================================================================ *)

(* ------ TROQUE O IP AQUI ------ *)
MQTT_FB_CONNECTION_CONFIG.sHostname     := '192.168.X.X';
MQTT_FB_CONNECTION_CONFIG.uiPort        := 1883;
MQTT_FB_CONNECTION_CONFIG.sClientId     := 'clp_mestre_gateway';
MQTT_FB_CONNECTION_CONFIG.bCleanSession := TRUE;

MQTT_FB.PUBLISH   := Pubs;
MQTT_FB.SUBSCRIBE := Subs;
MQTT_FB_Enable    := MQTT_FB.Enable;

MQTT_FB_Error             := MQTT_FB.ERROR;
MQTT_FB_State             := MQTT_FB.STATE;
MQTT_FB_Error_Code        := MQTT_FB.ERROR_CODE;
MQTT_FB_Pub_Status        := MQTT_FB.PUBLISH_STATUS;
MQTT_FB_Received_Messages := MQTT_FB.RECEIVED_MESSAGES;

(* Publicação: retorno do escravo → atualiza LEDs do app *)
FOR i := 1 TO 16 DO
    Pubs[i].sPublishTopic        := MQTT_TOPICS[i];
    Pubs[i].pbPublishPayload     := ADR(PUBS_PAYLOADS[i]);
    Pubs[i].uiPublishPayloadSize := TO_UINT(LEN(PUBS_PAYLOADS[i]));
    Pubs[i].uiPublishMessageQos  := MQTT_QOS_0;
    Pubs[i].bPublishRetain       := TRUE;

    IF (PUBS_PAYLOADS[i] <> PUBS_PAYLOADS_OLD[i]) THEN
        PUBS_PAYLOADS_OLD[i]     := PUBS_PAYLOADS[i];
        Pubs[i].bEnablePublish   := TRUE;
    END_IF

    IF (MQTT_FB_Pub_Status[i]) THEN
        Pubs[i].bEnablePublish   := FALSE;
    END_IF
END_FOR

(* Assinatura: recebe comandos do app *)
FOR i := 1 TO 16 DO
    Subs[i].eSubscribeTopic  := MQTT_TOPICS[i];
    Subs[i].pbPayloadBuffer  := ADR(SUBS_PAYLOADS[i]);
    Subs[i].uiMaxPayloadSize := SIZEOF(SUBS_PAYLOADS[i]);
    Subs[i].eSubscribeQos    := MQTT_QOS_0;
END_FOR

IF MQTT_FB_Error THEN
    MQTT_FB_Enable := PULSE_55;
ELSE
    MQTT_FB_Enable := TRUE;
END_IF

MQTT_FB();
