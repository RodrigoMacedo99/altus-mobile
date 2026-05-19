(*
  ARQUIVO: GVL_MQTT.st — CLP MESTRE (gateway)
  ONDE USAR: MasterTool > Application > UserGVLs > GVL_MQTT
  O QUE FAZ: variáveis MQTT do CLP mestre.
             O mestre só recebe comandos do app e publica o retorno do escravo.
             Quem executa as saídas físicas é o CLP escravo.
*)

VAR_GLOBAL

    (* Arrays internos da biblioteca LibMQTT — não mexa *)
    Pubs : ARRAY[1..gc_uiMaxPubs] OF MQTT_PUBLISH;
    Subs : ARRAY[1..gc_uiMaxSubs] OF MQTT_SUBSCRIBE;

    (* 16 tópicos — os mesmos para receber (subscribe) e publicar retorno (publish) *)
    MQTT_TOPICS : ARRAY[1..16] OF STRING := [
        'altus/kit1/pushbutton/1',   (* pos 1  → CMD_Q00 / kit1Led1 *)
        'altus/kit1/pushbutton/2',   (* pos 2  → CMD_Q01 / kit1Led2 *)
        'altus/kit1/pushbutton/3',   (* pos 3  → CMD_Q02 / kit1Led3 *)
        'altus/kit1/pushbutton/4',   (* pos 4  → CMD_Q03 / kit1Led4 *)
        'altus/kit1/switch/1',       (* pos 5  → CMD_Q04 / kit1Led5 *)
        'altus/kit1/switch/2',       (* pos 6  → CMD_Q05 / kit1Led6 *)
        'altus/kit1/switch/3',       (* pos 7  → CMD_Q06 / kit1Led7 *)
        'altus/kit1/switch/4',       (* pos 8  → CMD_Q07 / kit1Led8 *)
        'altus/kit2/pushbutton/1',   (* pos 9  → CMD_Q08 / kit2Led1 *)
        'altus/kit2/pushbutton/2',   (* pos 10 → CMD_Q09 / kit2Led2 *)
        'altus/kit2/pushbutton/3',   (* pos 11 → CMD_Q10 / kit2Led3 *)
        'altus/kit2/pushbutton/4',   (* pos 12 → CMD_Q11 / kit2Led4 *)
        'altus/kit2/switch/1',       (* pos 13 → CMD_Q12 / kit2Led5 *)
        'altus/kit2/switch/2',       (* pos 14 → CMD_Q13 / kit2Led6 *)
        'altus/kit2/switch/3',       (* pos 15 → CMD_Q14 / kit2Led7 *)
        'altus/kit2/switch/4'        (* pos 16 → CMD_Q15 / kit2Led8 *)
    ];

    (* O que chegou do app — payloads recebidos de cada tópico *)
    SUBS_PAYLOADS : ARRAY[1..gc_uiMaxSubs] OF STRING;

    (* O que vai publicar de volta — preenchido pelo MODBUS_GATEWAY com o retorno do escravo *)
    PUBS_PAYLOADS     : ARRAY[1..gc_uiMaxPubs] OF STRING;
    PUBS_PAYLOADS_OLD : ARRAY[1..gc_uiMaxPubs] OF STRING;

    (* Status internos *)
    MQTT_FB_Pub_Status        : ARRAY[1..gc_uiMaxPubs] OF BOOL;
    MQTT_FB_Received_Messages : ARRAY[1..gc_uiMaxSubs] OF MQTT_RECEIVED;

END_VAR
