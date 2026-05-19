(*
  ARQUIVO: MODBUS_MASTER.st
  ONDE USAR: MasterTool > pasta MQTT > MODBUS_MASTER (PRG)
  O QUE FAZ: pega o estado das saídas Q00–Q15 (definidas pelo MQTT) e
             empacota em dois registradores WORD para enviar ao CLP escravo
             via Modbus RTU sobre RS-485.

  FLUXO:
    App → MQTT → CLP mestre (XP340) → Modbus RS-485 → CLP escravo
                  [Q00–Q15 aqui]           [recebe os registradores]

  COMO FUNCIONA O EMPACOTAMENTO:
    Cada WORD tem 16 bits (0 a 15). Escrevemos TRUE/FALSE em cada bit.
    O CLP escravo lê o registrador e extrai os bits que precisa.

    Exemplo:
      MB_REG_KIT1 = 0000 0000 0000 0101  →  Q00=TRUE, Q02=TRUE, resto=FALSE
*)

(* ==============================================================
   Kit 1 — empacota Q00 a Q07 no registrador MB_REG_KIT1
   ============================================================== *)
MB_REG_KIT1.0 := Q00;   (* altus/kit1/pushbutton/1 *)
MB_REG_KIT1.1 := Q01;   (* altus/kit1/pushbutton/2 *)
MB_REG_KIT1.2 := Q02;   (* altus/kit1/pushbutton/3 *)
MB_REG_KIT1.3 := Q03;   (* altus/kit1/pushbutton/4 *)
MB_REG_KIT1.4 := Q04;   (* altus/kit1/switch/1     *)
MB_REG_KIT1.5 := Q05;   (* altus/kit1/switch/2     *)
MB_REG_KIT1.6 := Q06;   (* altus/kit1/switch/3     *)
MB_REG_KIT1.7 := Q07;   (* altus/kit1/switch/4     *)

(* ==============================================================
   Kit 2 — empacota Q08 a Q15 no registrador MB_REG_KIT2
   ============================================================== *)
MB_REG_KIT2.0 := Q08;   (* altus/kit2/pushbutton/1 *)
MB_REG_KIT2.1 := Q09;   (* altus/kit2/pushbutton/2 *)
MB_REG_KIT2.2 := Q10;   (* altus/kit2/pushbutton/3 *)
MB_REG_KIT2.3 := Q11;   (* altus/kit2/pushbutton/4 *)
MB_REG_KIT2.4 := Q12;   (* altus/kit2/switch/1     *)
MB_REG_KIT2.5 := Q13;   (* altus/kit2/switch/2     *)
MB_REG_KIT2.6 := Q14;   (* altus/kit2/switch/3     *)
MB_REG_KIT2.7 := Q15;   (* altus/kit2/switch/4     *)

(*
  A transmissão em si é feita pelo driver Modbus RTU configurado na
  árvore de hardware do MasterTool (seção COM 1 → Modbus Master).
  Não é necessário chamar nenhuma função aqui — o MasterTool envia
  MB_REG_KIT1 e MB_REG_KIT2 automaticamente a cada ciclo.
*)
