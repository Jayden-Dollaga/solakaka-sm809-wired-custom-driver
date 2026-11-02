// Program: SM809 mouse Software.exe
// Function: FUN_00406c60
// Entry: 00406c60
// Body: 00406c60 - 00406d1f
// Signature: undefined FUN_00406c60(void * this, int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_00406c60(void *this,int param_1)

{
  uint uVar1;
  uint uVar2;
  uint uVar3;
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00421761;
  local_10 = ExceptionList;
  uVar1 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  uVar3 = 0;
  local_14 = uVar1;
  do {
    if (*(int *)(param_1 + 0x108) == *(int *)((int)this + uVar3 * 4 + 0x20)) {
      DuiLib::CDuiString::CDuiString(local_98);
      local_8 = 0;
      uVar2 = uVar3 - 0x20;
      if (uVar3 < 0x20) {
        uVar2 = uVar3;
      }
      (**(code **)(**(int **)((int)this + uVar2 * 4 + 0x13c) + 0xf8))(1,uVar1);
      (**(code **)(**(int **)((int)this + 0x1bc) + 0xf8))(0);
      local_8 = 0xffffffff;
      DuiLib::CDuiString::~CDuiString(local_98);
    }
    uVar3 = uVar3 + 1;
  } while ((int)uVar3 < 0x40);
  ExceptionList = local_10;
  return;
}


