(*
  ARQUIVO: GVL_MQTT.st
  ONDE USAR: MasterTool > pasta MQTT > GVL_MQTT
  O QUE FAZ: declara todas as variáveis compartilhadas entre os programas MQTT
*)

VAR_GLOBAL

    (* Arrays internos da biblioteca LibMQTT — não mexa *)
    Pubs : ARRAY[1..gc_uiMaxPubs] OF MQTT_PUBLISH;
    Subs : ARRAY[1..gc_uiMaxSubs] OF MQTT_SUBSCRIBE;

    (* ---------------------------------------------------------------
       TÓPICOS — 16 no total (8 para Kit1, 8 para Kit2)
       A posição aqui define o índice usado nos outros programas.
       Publicar e assinar usam os MESMOS tópicos.
       --------------------------------------------------------------- *)
    MQTT_TOPICS : ARRAY[1..16] OF STRING := [
        (* Kit 1 - Botões (pushbutton) *)
        'altus/kit1/pushbutton/1',   (* pos 1  → Q00 / kit1Led1 *)
        'altus/kit1/pushbutton/2',   (* pos 2  → Q01 / kit1Led2 *)
        'altus/kit1/pushbutton/3',   (* pos 3  → Q02 / kit1Led3 *)
        'altus/kit1/pushbutton/4',   (* pos 4  → Q03 / kit1Led4 *)
        (* Kit 1 - Chaves (switch) *)
        'altus/kit1/switch/1',       (* pos 5  → Q04 / kit1Led5 *)
        'altus/kit1/switch/2',       (* pos 6  → Q05 / kit1Led6 *)
        'altus/kit1/switch/3',       (* pos 7  → Q06 / kit1Led7 *)
        'altus/kit1/switch/4',       (* pos 8  → Q07 / kit1Led8 *)
        (* Kit 2 - Botões (pushbutton) *)
        'altus/kit2/pushbutton/1',   (* pos 9  → Q08 / kit2Led1 *)
        'altus/kit2/pushbutton/2',   (* pos 10 → Q09 / kit2Led2 *)
        'altus/kit2/pushbutton/3',   (* pos 11 → Q10 / kit2Led3 *)
        'altus/kit2/pushbutton/4',   (* pos 12 → Q11 / kit2Led4 *)
        (* Kit 2 - Chaves (switch) *)
        'altus/kit2/switch/1',       (* pos 13 → Q12 / kit2Led5 *)
        'altus/kit2/switch/2',       (* pos 14 → Q13 / kit2Led6 *)
        'altus/kit2/switch/3',       (* pos 15 → Q14 / kit2Led7 *)
        'altus/kit2/switch/4'        (* pos 16 → Q15 / kit2Led8 *)
    ];

    (* Status internos — não mexa *)
    MQTT_FB_Pub_Status        : ARRAY[1..gc_uiMaxPubs] OF BOOL;
    MQTT_FB_Received_Messages : ARRAY[1..gc_uiMaxSubs] OF MQTT_RECEIVED;

    (* Payloads recebidos do app (o que chegou de cada tópico) *)
    SUBS_PAYLOADS : ARRAY[1..gc_uiMaxSubs] OF STRING;

    (* Payloads para publicar de volta (atualiza os LEDs do app) *)
    PUBS_PAYLOADS     : ARRAY[1..gc_uiMaxPubs] OF STRING;
    PUBS_PAYLOADS_OLD : ARRAY[1..gc_uiMaxPubs] OF STRING;

END_VAR
