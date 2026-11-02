// Program: SM809 mouse Software.exe
// Function: FUN_0041bd40
// Entry: 0041bd40
// Body: 0041bd40 - 0041bfcc
// Signature: undefined4 FUN_0041bd40(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

undefined4 __fastcall FUN_0041bd40(int param_1)

{
  int iVar1;
  undefined4 uVar2;
  bool bVar3;
  bool bVar4;
  bool bVar5;
  byte local_d0 [3];
  char local_cd;
  char local_cc;
  char local_cb;
  char local_ca;
  char local_c9;
  undefined4 local_8;
  
  local_8 = DAT_00432008 ^ (int)register0x00000010 - 4U;
  uVar2 = 0;
  memset(local_d0,0,200);
  local_d0[2] = 0;
  local_d0[0] = 7;
  local_d0[1] = 0;
  if (DAT_00432ad8 == 0xd07) {
    local_d0[2] = 0xa0 < *(int *)(DAT_00432aa0 + 0x88);
    if (0xa0 < *(int *)(DAT_00432aa0 + 0x8c)) {
      local_d0[2] = local_d0[2] | 2;
    }
    if (0xa0 < *(int *)(DAT_00432aa0 + 0x90)) {
      local_d0[2] = local_d0[2] | 4;
    }
    if (0xa0 < *(int *)(DAT_00432aa0 + 0x94)) {
      local_d0[2] = local_d0[2] | 8;
    }
    if (0xa0 < *(int *)(DAT_00432aa0 + 0x98)) {
      local_d0[2] = local_d0[2] | 0x10;
    }
    if (0xa0 < *(int *)(DAT_00432aa0 + 0x9c)) {
      local_d0[2] = local_d0[2] | 0x20;
    }
    if (0xa0 < *(int *)(DAT_00432aa0 + 0xa0)) {
      local_d0[2] = local_d0[2] | 0x40;
    }
    iVar1 = *(int *)(DAT_00432aa0 + 0xa4);
    bVar5 = SBORROW4(iVar1,0xa0);
    bVar4 = iVar1 + -0xa0 < 0;
    bVar3 = iVar1 == 0xa0;
  }
  else if (DAT_00432ad8 == 0xd2a) {
    local_d0[2] = 200 < *(int *)(DAT_00432aa0 + 0x88);
    if (200 < *(int *)(DAT_00432aa0 + 0x8c)) {
      local_d0[2] = local_d0[2] | 2;
    }
    if (200 < *(int *)(DAT_00432aa0 + 0x90)) {
      local_d0[2] = local_d0[2] | 4;
    }
    if (200 < *(int *)(DAT_00432aa0 + 0x94)) {
      local_d0[2] = local_d0[2] | 8;
    }
    if (200 < *(int *)(DAT_00432aa0 + 0x98)) {
      local_d0[2] = local_d0[2] | 0x10;
    }
    if (200 < *(int *)(DAT_00432aa0 + 0x9c)) {
      local_d0[2] = local_d0[2] | 0x20;
    }
    if (200 < *(int *)(DAT_00432aa0 + 0xa0)) {
      local_d0[2] = local_d0[2] | 0x40;
    }
    iVar1 = *(int *)(DAT_00432aa0 + 0xa4);
    bVar5 = SBORROW4(iVar1,200);
    bVar4 = iVar1 + -200 < 0;
    bVar3 = iVar1 == 200;
  }
  else {
    if (DAT_00432ad8 != 0xcef) goto LAB_0041bf5a;
    local_d0[2] = 0x78 < *(int *)(DAT_00432aa0 + 0x88);
    if (0x78 < *(int *)(DAT_00432aa0 + 0x8c)) {
      local_d0[2] = local_d0[2] | 2;
    }
    if (0x78 < *(int *)(DAT_00432aa0 + 0x90)) {
      local_d0[2] = local_d0[2] | 4;
    }
    if (0x78 < *(int *)(DAT_00432aa0 + 0x94)) {
      local_d0[2] = local_d0[2] | 8;
    }
    if (0x78 < *(int *)(DAT_00432aa0 + 0x98)) {
      local_d0[2] = local_d0[2] | 0x10;
    }
    if (0x78 < *(int *)(DAT_00432aa0 + 0x9c)) {
      local_d0[2] = local_d0[2] | 0x20;
    }
    if (0x78 < *(int *)(DAT_00432aa0 + 0xa0)) {
      local_d0[2] = local_d0[2] | 0x40;
    }
    iVar1 = *(int *)(DAT_00432aa0 + 0xa4);
    bVar5 = SBORROW4(iVar1,0x78);
    bVar4 = iVar1 + -0x78 < 0;
    bVar3 = iVar1 == 0x78;
  }
  if (!bVar3 && bVar5 == bVar4) {
    local_d0[2] = local_d0[2] | 0x80;
  }
LAB_0041bf5a:
  local_c9 = ((((-8 - local_ca) - local_cd) - local_cc) - local_cb) - local_d0[2];
  if (*(int *)(param_1 + 0x1af0) != 0) {
    FUN_00414710(local_d0);
  }
  if (DAT_00432acc != 0) {
    uVar2 = (**(code **)(param_1 + 0x788))(local_d0,8);
  }
  Sleep(0x14);
  return uVar2;
}


