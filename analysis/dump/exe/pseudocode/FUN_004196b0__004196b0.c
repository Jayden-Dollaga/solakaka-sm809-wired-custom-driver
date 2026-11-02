// Program: SM809 mouse Software.exe
// Function: FUN_004196b0
// Entry: 004196b0
// Body: 004196b0 - 00419855
// Signature: int FUN_004196b0(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

int __fastcall FUN_004196b0(int param_1)

{
  int iVar1;
  byte local_d0;
  char local_cf;
  char local_ce;
  byte local_cd;
  char local_cc;
  char local_cb;
  char local_ca;
  char local_c9;
  undefined4 local_8;
  
  local_8 = DAT_00432008 ^ (int)register0x00000010 - 4U;
  memset(&local_d0,0,200);
  local_d0 = 0x83;
  local_c9 = ((((('|' - local_cf) - local_ce) - local_cd) - local_cc) - local_cb) - local_ca;
  if (*(int *)(param_1 + 0x1af0) != 0) {
    FUN_00414710(&local_d0);
  }
  (**(code **)(param_1 + 0x788))(&local_d0,8);
  memset(&local_d0,0,200);
  local_d0 = 0x8b;
  local_c9 = ((((('t' - local_cf) - local_ce) - local_cd) - local_cc) - local_cb) - local_ca;
  if (*(int *)(param_1 + 0x1af0) != 0) {
    FUN_00414710(&local_d0);
  }
  (**(code **)(param_1 + 0x78c))(&local_d0,8);
  if (*(int *)(param_1 + 0x1af0) != 0) {
    FUN_00414810(&local_d0);
  }
  local_d0 = 3;
  local_cc = 0x40;
  local_cd = (*(int *)(DAT_00432aa0 + 0x134) != 1) - 1U & 8 | local_cd & 0xf7;
  local_c9 = ((((-0x44 - local_cd) - local_cf) - local_ce) - local_cb) - local_ca;
  if (*(int *)(param_1 + 0x1af0) != 0) {
    FUN_00414710(&local_d0);
  }
  iVar1 = (**(code **)(param_1 + 0x788))(&local_d0,8);
  if (iVar1 != 0) {
    Sleep(0x14);
  }
  return iVar1;
}


