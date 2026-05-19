(*
  ARQUIVO: ESCRAVO_RETORNO.st — CLP ESCRAVO
  ONDE USAR: MasterTool (projeto do escravo) > Application > ESCRAVO_RETORNO (PRG)
  O QUE FAZ: lê o estado REAL das saídas físicas e escreve nos registradores
             de retorno (MB_FB_*), que o mestre vai ler via Modbus (FC03).
             O mestre então publica esses valores no MQTT → LEDs do app atualizam.

  POR QUE ISSO EXISTE:
    O app pediu "ligue Q00". O escravo ligou. Mas e se a saída travou?
    O retorno garante que o LED do app reflita o estado REAL do hardware,
    não apenas o que foi pedido.

  NOTA: se quiser retornar também leituras de entradas (sensores, botões físicos),
        adicione abaixo da mesma forma usando I00, AI0, etc.
*)

(* ==============================================================
   Kit 1 — empacota estado real de Q00-Q07 em MB_FB_KIT1
   ============================================================== *)
MB_FB_KIT1.0 := Q00;
MB_FB_KIT1.1 := Q01;
MB_FB_KIT1.2 := Q02;
MB_FB_KIT1.3 := Q03;
MB_FB_KIT1.4 := Q04;
MB_FB_KIT1.5 := Q05;
MB_FB_KIT1.6 := Q06;
MB_FB_KIT1.7 := Q07;

(* ==============================================================
   Kit 2 — empacota estado real de Q08-Q15 em MB_FB_KIT2
   ============================================================== *)
MB_FB_KIT2.0 := Q08;
MB_FB_KIT2.1 := Q09;
MB_FB_KIT2.2 := Q10;
MB_FB_KIT2.3 := Q11;
MB_FB_KIT2.4 := Q12;
MB_FB_KIT2.5 := Q13;
MB_FB_KIT2.6 := Q14;
MB_FB_KIT2.7 := Q15;

(*
  EXEMPLO — retornar entrada analógica (opcional):
  Se quiser enviar também o valor de um sensor, declare um registrador extra
  na GVL_ESCRAVO (ex: MB_FB_SENSOR : WORD) e faça:

    MB_FB_SENSOR := AI0;  (* valor bruto do sensor analógico *)

  No mestre, mapeie o registrador correspondente e publique em um tópico MQTT.
*)
