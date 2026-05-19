(*
  ARQUIVO: GVL_MODBUS.st — CLP MESTRE (gateway)
  ONDE USAR: MasterTool > Application > UserGVLs > GVL_MODBUS
  O QUE FAZ: registradores Modbus do mestre.

  DIREÇÃO DOS REGISTRADORES:
    MB_CMD_*  → mestre ESCREVE no escravo  (FC16 - Write Multiple Registers)
                  contém os comandos recebidos do app via MQTT
    MB_FB_*   → mestre LÊ do escravo       (FC03 - Read Holding Registers)
                  contém o estado real das saídas executadas pelo escravo

  ENDEREÇOS NO ESCRAVO:
    MB_CMD_KIT1 → Holding Register 40001 (endereço 0)
    MB_CMD_KIT2 → Holding Register 40002 (endereço 1)
    MB_FB_KIT1  → Holding Register 40003 (endereço 2)
    MB_FB_KIT2  → Holding Register 40004 (endereço 3)
*)

VAR_GLOBAL

    (* --- COMANDOS: mestre envia ao escravo (app → mestre → escravo) --- *)
    (* Cada bit representa uma saída. Bit 0 = Kit1/pushbutton/1, etc. *)
    MB_CMD_KIT1 : WORD;   (* bits 0-7: CMD_Q00 a CMD_Q07 *)
    MB_CMD_KIT2 : WORD;   (* bits 0-7: CMD_Q08 a CMD_Q15 *)

    (* --- RETORNO: mestre lê do escravo (escravo → mestre → app) --- *)
    (* Preenchido pelo escravo com o estado real das saídas físicas *)
    MB_FB_KIT1  : WORD;   (* bits 0-7: estado real Q00-Q07 no escravo *)
    MB_FB_KIT2  : WORD;   (* bits 0-7: estado real Q08-Q15 no escravo *)

    (* Comandos individuais (BOOL) — preenchidos pelo MQTT_RECEBER *)
    CMD_Q00 : BOOL;   CMD_Q01 : BOOL;   CMD_Q02 : BOOL;   CMD_Q03 : BOOL;
    CMD_Q04 : BOOL;   CMD_Q05 : BOOL;   CMD_Q06 : BOOL;   CMD_Q07 : BOOL;
    CMD_Q08 : BOOL;   CMD_Q09 : BOOL;   CMD_Q10 : BOOL;   CMD_Q11 : BOOL;
    CMD_Q12 : BOOL;   CMD_Q13 : BOOL;   CMD_Q14 : BOOL;   CMD_Q15 : BOOL;

END_VAR
