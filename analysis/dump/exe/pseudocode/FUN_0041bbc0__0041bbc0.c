// Program: SM809 mouse Software.exe
// Function: FUN_0041bbc0
// Entry: 0041bbc0
// Body: 0041bbc0 - 0041bd33
// Signature: undefined4 FUN_0041bbc0(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

undefined4 __fastcall FUN_0041bbc0(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined2 local_328;
  undefined1 local_326 [198];
  byte local_260 [200];
  undefined1 local_198;
  byte local_197 [5];
  char local_192;
  char local_191;
  byte local_d0 [6];
  char local_ca;
  char local_c9;
  undefined4 local_8;
  
  local_8 = DAT_00432008 ^ (int)register0x00000010 - 4U;
  memset(&local_198,0,200);
  local_197[0] = 0xaa;
  local_197[1] = 0xdd;
  local_197[2] = 0x3b;
  local_197[3] = 0x62;
  local_191 = (-0x25 - local_192) - local_197[4];
  (**(code **)(param_1 + 0x788))(&local_198,8);
  Sleep(0x1e);
  memset(local_326,0,0xc6);
  local_328 = 0;
  (**(code **)(param_1 + 0x78c))(&local_328,8);
  Sleep(0x1e);
  memset(local_d0,0,200);
  local_d0[1] = 0xaa;
  local_d0[2] = 0xdd;
  local_d0[3] = 0x3b;
  local_d0[4] = 0x62;
  local_c9 = (-0x25 - local_ca) - local_d0[5];
  FUN_00414710(local_d0);
  (**(code **)(param_1 + 0x788))(local_d0,8);
  Sleep(0x1e);
  memset(local_260 + 2,0,0xc6);
  local_260[0] = 0;
  local_260[1] = 0;
  uVar1 = (**(code **)(param_1 + 0x78c))(local_260,8);
  FUN_00414810(local_260);
  iVar2 = 0;
  do {
    if (local_260[iVar2 + 1] != local_197[iVar2]) {
      *(undefined4 *)(param_1 + 0x16d0) = 0;
      return uVar1;
    }
    iVar2 = iVar2 + 1;
  } while (iVar2 < 4);
  return uVar1;
}


