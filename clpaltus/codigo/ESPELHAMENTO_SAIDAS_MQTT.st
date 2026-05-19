(*
  ARQUIVO: ESPELHAMENTO_SAIDAS_MQTT.st
  ONDE USAR: MasterTool > pasta MQTT > ESPELHAMENTO_SAIDAS_MQTT (PRG)

  O QUE FAZ:
    1. Lê o que chegou do app (SUBS_PAYLOADS) e liga/desliga as saídas do CLP
    2. Publica de volta o estado real de cada saída (PUBS_PAYLOADS)
       → isso é o que acende/apaga os LEDs no app

  MAPEAMENTO COMPLETO:
    Posição | Tópico                      | Saída CLP | LED no app
    --------|-----------------------------|-----------|------------
       1    | altus/kit1/pushbutton/1     |    Q00    | kit1Led1
       2    | altus/kit1/pushbutton/2     |    Q01    | kit1Led2
       3    | altus/kit1/pushbutton/3     |    Q02    | kit1Led3
       4    | altus/kit1/pushbutton/4     |    Q03    | kit1Led4
       5    | altus/kit1/switch/1         |    Q04    | kit1Led5
       6    | altus/kit1/switch/2         |    Q05    | kit1Led6
       7    | altus/kit1/switch/3         |    Q06    | kit1Led7
       8    | altus/kit1/switch/4         |    Q07    | kit1Led8
       9    | altus/kit2/pushbutton/1     |    Q08    | kit2Led1
      10    | altus/kit2/pushbutton/2     |    Q09    | kit2Led2
      11    | altus/kit2/pushbutton/3     |    Q10    | kit2Led3
      12    | altus/kit2/pushbutton/4     |    Q11    | kit2Led4
      13    | altus/kit2/switch/1         |    Q12    | kit2Led5
      14    | altus/kit2/switch/2         |    Q13    | kit2Led6
      15    | altus/kit2/switch/3         |    Q14    | kit2Led7
      16    | altus/kit2/switch/4         |    Q15    | kit2Led8
*)

(* ==============================================================
   PARTE 1 — Recebe comando do app e atua nas saídas do CLP
   '1' = ligar, '0' = desligar
   ============================================================== *)

(* Kit 1 - Botões *)
Q00 := (SUBS_PAYLOADS[1]  = '1');
Q01 := (SUBS_PAYLOADS[2]  = '1');
Q02 := (SUBS_PAYLOADS[3]  = '1');
Q03 := (SUBS_PAYLOADS[4]  = '1');

(* Kit 1 - Chaves *)
Q04 := (SUBS_PAYLOADS[5]  = '1');
Q05 := (SUBS_PAYLOADS[6]  = '1');
Q06 := (SUBS_PAYLOADS[7]  = '1');
Q07 := (SUBS_PAYLOADS[8]  = '1');

(* Kit 2 - Botões *)
Q08 := (SUBS_PAYLOADS[9]  = '1');
Q09 := (SUBS_PAYLOADS[10] = '1');
Q10 := (SUBS_PAYLOADS[11] = '1');
Q11 := (SUBS_PAYLOADS[12] = '1');

(* Kit 2 - Chaves *)
Q12 := (SUBS_PAYLOADS[13] = '1');
Q13 := (SUBS_PAYLOADS[14] = '1');
Q14 := (SUBS_PAYLOADS[15] = '1');
Q15 := (SUBS_PAYLOADS[16] = '1');


(* ==============================================================
   PARTE 2 — Publica o estado real das saídas de volta ao broker
   Isso é o que faz os LEDs do app acenderem/apagarem.
   SEL(condição, valor_se_falso, valor_se_verdadeiro)
   ============================================================== *)

(* Kit 1 - Botões *)
PUBS_PAYLOADS[1]  := SEL(Q00, '0', '1');
PUBS_PAYLOADS[2]  := SEL(Q01, '0', '1');
PUBS_PAYLOADS[3]  := SEL(Q02, '0', '1');
PUBS_PAYLOADS[4]  := SEL(Q03, '0', '1');

(* Kit 1 - Chaves *)
PUBS_PAYLOADS[5]  := SEL(Q04, '0', '1');
PUBS_PAYLOADS[6]  := SEL(Q05, '0', '1');
PUBS_PAYLOADS[7]  := SEL(Q06, '0', '1');
PUBS_PAYLOADS[8]  := SEL(Q07, '0', '1');

(* Kit 2 - Botões *)
PUBS_PAYLOADS[9]  := SEL(Q08, '0', '1');
PUBS_PAYLOADS[10] := SEL(Q09, '0', '1');
PUBS_PAYLOADS[11] := SEL(Q10, '0', '1');
PUBS_PAYLOADS[12] := SEL(Q11, '0', '1');

(* Kit 2 - Chaves *)
PUBS_PAYLOADS[13] := SEL(Q12, '0', '1');
PUBS_PAYLOADS[14] := SEL(Q13, '0', '1');
PUBS_PAYLOADS[15] := SEL(Q14, '0', '1');
PUBS_PAYLOADS[16] := SEL(Q15, '0', '1');
