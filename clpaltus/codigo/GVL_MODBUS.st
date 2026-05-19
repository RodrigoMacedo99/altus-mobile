(*
  ARQUIVO: GVL_MODBUS.st
  ONDE USAR: MasterTool > Application > UserGVLs > GVL_MODBUS
  O QUE FAZ: declara as variáveis usadas na comunicação Modbus RTU via RS-485

  IMPORTANTE: as variáveis MB_REG_KIT1 e MB_REG_KIT2 precisam ser mapeadas
  na configuração de hardware do MasterTool para os registradores do CLP escravo.
  Veja o GUIA_PASSO_A_PASSO.md seção "PARTE 3 — Configurar Modbus RS-485".
*)

VAR_GLOBAL

    (* ---------------------------------------------------------------
       Registradores enviados ao CLP escravo via Modbus RTU
       Cada WORD carrega 16 bits — usamos os 8 primeiros de cada um.

       MB_REG_KIT1 — bits mapeados para Kit 1:
         bit 0 = Q00 (pushbutton/1)    bit 4 = Q04 (switch/1)
         bit 1 = Q01 (pushbutton/2)    bit 5 = Q05 (switch/2)
         bit 2 = Q02 (pushbutton/3)    bit 6 = Q06 (switch/3)
         bit 3 = Q03 (pushbutton/4)    bit 7 = Q07 (switch/4)

       MB_REG_KIT2 — bits mapeados para Kit 2:
         bit 0 = Q08 (pushbutton/1)    bit 4 = Q12 (switch/1)
         bit 1 = Q09 (pushbutton/2)    bit 5 = Q13 (switch/2)
         bit 2 = Q10 (pushbutton/3)    bit 6 = Q14 (switch/3)
         bit 3 = Q11 (pushbutton/4)    bit 7 = Q15 (switch/4)
       --------------------------------------------------------------- *)
    MB_REG_KIT1 : WORD;   (* Registrador 40001 no CLP escravo *)
    MB_REG_KIT2 : WORD;   (* Registrador 40002 no CLP escravo *)

    (* Status da comunicação Modbus — para monitorar no MasterTool *)
    MB_CONNECTED : BOOL;  (* TRUE quando escravo responde *)
    MB_ERROR     : BOOL;  (* TRUE quando há falha de comunicação *)

END_VAR
