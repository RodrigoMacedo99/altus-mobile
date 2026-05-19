(*
  ARQUIVO: GVL_ESCRAVO.st — CLP ESCRAVO
  ONDE USAR: MasterTool (projeto do escravo) > Application > UserGVLs > GVL_ESCRAVO
  O QUE FAZ: declara os registradores Modbus do escravo.

  O MESTRE ESCREVE em MB_CMD_* e LÊ de MB_FB_*.
  O ESCRAVO LÊ de MB_CMD_* e ESCREVE em MB_FB_*.

  ENDEREÇOS MODBUS (configurar na árvore de hardware do escravo):
    MB_CMD_KIT1 → Holding Register endereço 0  (mestre escreve aqui)
    MB_CMD_KIT2 → Holding Register endereço 1  (mestre escreve aqui)
    MB_FB_KIT1  → Holding Register endereço 2  (mestre lê daqui)
    MB_FB_KIT2  → Holding Register endereço 3  (mestre lê daqui)
*)

VAR_GLOBAL

    (* Registradores de COMANDO — escritos pelo mestre, lidos pelo escravo *)
    MB_CMD_KIT1 : WORD;   (* bits 0-7: Q00-Q07 a executar *)
    MB_CMD_KIT2 : WORD;   (* bits 0-7: Q08-Q15 a executar *)

    (* Registradores de RETORNO — escritos pelo escravo, lidos pelo mestre *)
    (* Contêm o estado real das saídas físicas após execução *)
    MB_FB_KIT1  : WORD;   (* bits 0-7: estado atual Q00-Q07 *)
    MB_FB_KIT2  : WORD;   (* bits 0-7: estado atual Q08-Q15 *)

END_VAR
