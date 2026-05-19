(*
  ARQUIVO: MODBUS_GATEWAY.st — CLP MESTRE (gateway)
  ONDE USAR: MasterTool > pasta MQTT > MODBUS_GATEWAY (PRG)
  O QUE FAZ:
    1. Empacota os comandos (CMD_Q*) em registradores WORD para enviar ao escravo
    2. Desempacota o retorno (MB_FB_*) do escravo e prepara para publicar no MQTT

  FLUXO:
    App → MQTT → SUBS_PAYLOADS → MQTT_RECEBER → CMD_Q* (BOOL)
                                                       ↓  [aqui]
                                               MB_CMD_KIT1/2 (WORD)
                                                       ↓  [RS-485]
                                               CLP Escravo executa
                                                       ↓  [RS-485]
                                               MB_FB_KIT1/2 (WORD)
                                                       ↓  [aqui]
                                               PUBS_PAYLOADS → MQTT → LEDs do app
*)

(* ==============================================================
   PARTE 1 — Empacota comandos → envia ao escravo via Modbus
   O MasterTool escreve MB_CMD_KIT1/2 no escravo automaticamente (FC16)
   ============================================================== *)

(* Kit 1 → MB_CMD_KIT1 *)
MB_CMD_KIT1.0 := CMD_Q00;
MB_CMD_KIT1.1 := CMD_Q01;
MB_CMD_KIT1.2 := CMD_Q02;
MB_CMD_KIT1.3 := CMD_Q03;
MB_CMD_KIT1.4 := CMD_Q04;
MB_CMD_KIT1.5 := CMD_Q05;
MB_CMD_KIT1.6 := CMD_Q06;
MB_CMD_KIT1.7 := CMD_Q07;

(* Kit 2 → MB_CMD_KIT2 *)
MB_CMD_KIT2.0 := CMD_Q08;
MB_CMD_KIT2.1 := CMD_Q09;
MB_CMD_KIT2.2 := CMD_Q10;
MB_CMD_KIT2.3 := CMD_Q11;
MB_CMD_KIT2.4 := CMD_Q12;
MB_CMD_KIT2.5 := CMD_Q13;
MB_CMD_KIT2.6 := CMD_Q14;
MB_CMD_KIT2.7 := CMD_Q15;


(* ==============================================================
   PARTE 2 — Desempacota retorno do escravo → prepara publicação MQTT
   O MasterTool lê MB_FB_KIT1/2 do escravo automaticamente (FC03).
   Aqui convertemos os bits de volta para '0'/'1' (string) para o MQTT.
   SEL(condição, valor_se_falso, valor_se_verdadeiro)
   ============================================================== *)

(* Kit 1 ← MB_FB_KIT1 *)
PUBS_PAYLOADS[1]  := SEL(MB_FB_KIT1.0, '0', '1');
PUBS_PAYLOADS[2]  := SEL(MB_FB_KIT1.1, '0', '1');
PUBS_PAYLOADS[3]  := SEL(MB_FB_KIT1.2, '0', '1');
PUBS_PAYLOADS[4]  := SEL(MB_FB_KIT1.3, '0', '1');
PUBS_PAYLOADS[5]  := SEL(MB_FB_KIT1.4, '0', '1');
PUBS_PAYLOADS[6]  := SEL(MB_FB_KIT1.5, '0', '1');
PUBS_PAYLOADS[7]  := SEL(MB_FB_KIT1.6, '0', '1');
PUBS_PAYLOADS[8]  := SEL(MB_FB_KIT1.7, '0', '1');

(* Kit 2 ← MB_FB_KIT2 *)
PUBS_PAYLOADS[9]  := SEL(MB_FB_KIT2.0, '0', '1');
PUBS_PAYLOADS[10] := SEL(MB_FB_KIT2.1, '0', '1');
PUBS_PAYLOADS[11] := SEL(MB_FB_KIT2.2, '0', '1');
PUBS_PAYLOADS[12] := SEL(MB_FB_KIT2.3, '0', '1');
PUBS_PAYLOADS[13] := SEL(MB_FB_KIT2.4, '0', '1');
PUBS_PAYLOADS[14] := SEL(MB_FB_KIT2.5, '0', '1');
PUBS_PAYLOADS[15] := SEL(MB_FB_KIT2.6, '0', '1');
PUBS_PAYLOADS[16] := SEL(MB_FB_KIT2.7, '0', '1');
