(*
  ARQUIVO: MQTT_RECEBER.st — CLP MESTRE (gateway)
  ONDE USAR: MasterTool > pasta MQTT > MQTT_RECEBER (PRG)
  O QUE FAZ: converte os payloads recebidos do app em variáveis BOOL (CMD_Q*).
             Essas variáveis são lidas pelo MODBUS_GATEWAY para enviar ao escravo.

  NOTA: o mestre NÃO aciona saídas físicas próprias — apenas passa o comando adiante.
*)

(* Kit 1 - Botões *)
CMD_Q00 := (SUBS_PAYLOADS[1]  = '1');
CMD_Q01 := (SUBS_PAYLOADS[2]  = '1');
CMD_Q02 := (SUBS_PAYLOADS[3]  = '1');
CMD_Q03 := (SUBS_PAYLOADS[4]  = '1');

(* Kit 1 - Chaves *)
CMD_Q04 := (SUBS_PAYLOADS[5]  = '1');
CMD_Q05 := (SUBS_PAYLOADS[6]  = '1');
CMD_Q06 := (SUBS_PAYLOADS[7]  = '1');
CMD_Q07 := (SUBS_PAYLOADS[8]  = '1');

(* Kit 2 - Botões *)
CMD_Q08 := (SUBS_PAYLOADS[9]  = '1');
CMD_Q09 := (SUBS_PAYLOADS[10] = '1');
CMD_Q10 := (SUBS_PAYLOADS[11] = '1');
CMD_Q11 := (SUBS_PAYLOADS[12] = '1');

(* Kit 2 - Chaves *)
CMD_Q12 := (SUBS_PAYLOADS[13] = '1');
CMD_Q13 := (SUBS_PAYLOADS[14] = '1');
CMD_Q14 := (SUBS_PAYLOADS[15] = '1');
CMD_Q15 := (SUBS_PAYLOADS[16] = '1');
