(*
  ARQUIVO: MQTT.st
  ONDE USAR: MasterTool > pasta MQTT > MQTT (PRG)
  O QUE FAZ: configura a conexão com o broker Mosquitto e mantém ela ativa.

  !! ATENÇÃO !!
  Antes de carregar no CLP, você PRECISA trocar o IP abaixo.
  Para descobrir o IP do seu PC: abra o CMD e digite "ipconfig"
  Procure por "Endereço IPv4" (exemplo: 192.168.1.100)
*)

(* ===== SEÇÃO VAR — cole na parte de CIMA do editor ===== *)
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

(* ===== CÓDIGO — cole na parte de BAIXO do editor ===== *)

(* ------ TROQUE O IP AQUI ------
   sHostname = IP do PC onde o Mosquitto está rodando
   Exemplo:   '192.168.1.100'
   -------------------------------- *)
MQTT_FB_CONNECTION_CONFIG.sHostname     := '192.168.X.X';
MQTT_FB_CONNECTION_CONFIG.uiPort        := 1883;
MQTT_FB_CONNECTION_CONFIG.sClientId     := 'clp_xp340_kit1';
MQTT_FB_CONNECTION_CONFIG.bCleanSession := TRUE;

(* Aponta os arrays declarados na GVL_MQTT *)
MQTT_FB.PUBLISH   := Pubs;
MQTT_FB.SUBSCRIBE := Subs;

(* Habilita a função MQTT *)
MQTT_FB_Enable := MQTT_FB.Enable;

(* Lê os status de erro e conexão *)
MQTT_FB_Error             := MQTT_FB.ERROR;
MQTT_FB_State             := MQTT_FB.STATE;
MQTT_FB_Error_Code        := MQTT_FB.ERROR_CODE;
MQTT_FB_Pub_Status        := MQTT_FB.PUBLISH_STATUS;
MQTT_FB_Received_Messages := MQTT_FB.RECEIVED_MESSAGES;

(* Configura as assinaturas — o CLP vai escutar estes 8 tópicos *)
FOR i := 1 TO 8 DO
    Subs[i].eSubscribeTopic  := SUBSCRIBE_TOPICS[i];
    Subs[i].pbPayloadBuffer  := ADR(SUBS_PAYLOADS[i]);
    Subs[i].uiMaxPayloadSize := SIZEOF(SUBS_PAYLOADS[i]);
    Subs[i].eSubscribeQos    := MQTT_QOS_0;
END_FOR

(* Reconecta automaticamente se cair a conexão *)
IF MQTT_FB_Error THEN
    MQTT_FB_Enable := PULSE_55;
ELSE
    MQTT_FB_Enable := TRUE;
END_IF

(* Chama a função — deve ser a última linha *)
MQTT_FB();
