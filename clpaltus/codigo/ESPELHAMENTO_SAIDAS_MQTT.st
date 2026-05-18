(*
  ARQUIVO: ESPELHAMENTO_SAIDAS_MQTT.st
  ONDE USAR: MasterTool > pasta MQTT > ESPELHAMENTO_SAIDAS_MQTT (PRG)
  O QUE FAZ: quando o app manda "1" em um tópico, liga a saída correspondente.
             quando manda "0", desliga.

  MAPEAMENTO:
    App publica em...             CLP liga/desliga...
    altus/kit1/pushbutton/1   →   Q00
    altus/kit1/pushbutton/2   →   Q01
    altus/kit1/pushbutton/3   →   Q02
    altus/kit1/pushbutton/4   →   Q03
    altus/kit1/switch/1       →   Q04
    altus/kit1/switch/2       →   Q05
    altus/kit1/switch/3       →   Q06
    altus/kit1/switch/4       →   Q07
*)

(* Kit 1 - Botões (pushbutton) *)
Q00 := (SUBS_PAYLOADS[1] = '1');
Q01 := (SUBS_PAYLOADS[2] = '1');
Q02 := (SUBS_PAYLOADS[3] = '1');
Q03 := (SUBS_PAYLOADS[4] = '1');

(* Kit 1 - Chaves (switch) *)
Q04 := (SUBS_PAYLOADS[5] = '1');
Q05 := (SUBS_PAYLOADS[6] = '1');
Q06 := (SUBS_PAYLOADS[7] = '1');
Q07 := (SUBS_PAYLOADS[8] = '1');
