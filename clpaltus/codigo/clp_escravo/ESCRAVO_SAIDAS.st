(*
  ARQUIVO: ESCRAVO_SAIDAS.st — CLP ESCRAVO
  ONDE USAR: MasterTool (projeto do escravo) > Application > ESCRAVO_SAIDAS (PRG)
  O QUE FAZ: lê os registradores de comando recebidos do mestre via Modbus RS-485
             e aciona as saídas físicas do CLP escravo.

  ORIGEM DOS DADOS:
    MB_CMD_KIT1 e MB_CMD_KIT2 são escritos automaticamente pelo mestre (FC16).
    Cada bit representa o estado que o app pediu para aquela saída.
*)

(* ==============================================================
   Kit 1 — extrai bits de MB_CMD_KIT1 → saídas Q00 a Q07
   ============================================================== *)
Q00 := MB_CMD_KIT1.0;   (* altus/kit1/pushbutton/1 *)
Q01 := MB_CMD_KIT1.1;   (* altus/kit1/pushbutton/2 *)
Q02 := MB_CMD_KIT1.2;   (* altus/kit1/pushbutton/3 *)
Q03 := MB_CMD_KIT1.3;   (* altus/kit1/pushbutton/4 *)
Q04 := MB_CMD_KIT1.4;   (* altus/kit1/switch/1     *)
Q05 := MB_CMD_KIT1.5;   (* altus/kit1/switch/2     *)
Q06 := MB_CMD_KIT1.6;   (* altus/kit1/switch/3     *)
Q07 := MB_CMD_KIT1.7;   (* altus/kit1/switch/4     *)

(* ==============================================================
   Kit 2 — extrai bits de MB_CMD_KIT2 → saídas Q08 a Q15
   ============================================================== *)
Q08 := MB_CMD_KIT2.0;   (* altus/kit2/pushbutton/1 *)
Q09 := MB_CMD_KIT2.1;   (* altus/kit2/pushbutton/2 *)
Q10 := MB_CMD_KIT2.2;   (* altus/kit2/pushbutton/3 *)
Q11 := MB_CMD_KIT2.3;   (* altus/kit2/pushbutton/4 *)
Q12 := MB_CMD_KIT2.4;   (* altus/kit2/switch/1     *)
Q13 := MB_CMD_KIT2.5;   (* altus/kit2/switch/2     *)
Q14 := MB_CMD_KIT2.6;   (* altus/kit2/switch/3     *)
Q15 := MB_CMD_KIT2.7;   (* altus/kit2/switch/4     *)
