(*
  ARQUIVO: GVL_MQTT.st
  ONDE USAR: MasterTool > pasta MQTT > GVL_MQTT
  O QUE FAZ: declara todas as variáveis que os outros programas vão usar
*)

VAR_GLOBAL

    (* Arrays internos da biblioteca LibMQTT — não mexa *)
    Pubs : ARRAY[1..gc_uiMaxPubs] OF MQTT_PUBLISH;
    Subs : ARRAY[1..gc_uiMaxSubs] OF MQTT_SUBSCRIBE;

    (* Tópicos que o CLP vai ESCUTAR (receber do app) *)
    (* Ordem importa: posição 1 aqui = posição 1 no ESPELHAMENTO_SAIDAS *)
    SUBSCRIBE_TOPICS : ARRAY[1..8] OF STRING := [
        'altus/kit1/pushbutton/1',   (* posição 1 → vai para Q00 *)
        'altus/kit1/pushbutton/2',   (* posição 2 → vai para Q01 *)
        'altus/kit1/pushbutton/3',   (* posição 3 → vai para Q02 *)
        'altus/kit1/pushbutton/4',   (* posição 4 → vai para Q03 *)
        'altus/kit1/switch/1',       (* posição 5 → vai para Q04 *)
        'altus/kit1/switch/2',       (* posição 6 → vai para Q05 *)
        'altus/kit1/switch/3',       (* posição 7 → vai para Q06 *)
        'altus/kit1/switch/4'        (* posição 8 → vai para Q07 *)
    ];

    (* Status internos — não mexa *)
    MQTT_FB_Pub_Status        : ARRAY[1..gc_uiMaxPubs] OF BOOL;
    MQTT_FB_Received_Messages : ARRAY[1..gc_uiMaxSubs] OF MQTT_RECEIVED;

    (* Aqui ficam os valores que chegam do app (payload de cada tópico) *)
    SUBS_PAYLOADS : ARRAY[1..gc_uiMaxSubs] OF STRING;

END_VAR
