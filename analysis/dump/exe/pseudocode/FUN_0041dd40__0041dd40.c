// Program: SM809 mouse Software.exe
// Function: FUN_0041dd40
// Entry: 0041dd40
// Body: 0041dd40 - 0041de7b
// Signature: undefined FUN_0041dd40(void * this, uint param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_0041dd40(void *this,uint param_1)

{
  int iVar1;
  uint uVar2;
  wchar_t *pwVar3;
  CDuiString *this_00;
  CDuiString *this_01;
  CDuiString *this_02;
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00421c31;
  local_10 = ExceptionList;
  uVar2 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  local_14 = uVar2;
  DuiLib::CDuiString::CDuiString(local_98);
  local_8 = 0;
  DuiLib::CDuiString::Format(this_00,(wchar_t *)local_98,&DAT_00424f54,param_1 & 0xff,uVar2);
  iVar1 = **(int **)((int)this + 0x774);
  pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
  (**(code **)(iVar1 + 0x2c))(pwVar3);
  DuiLib::CDuiString::Format(this_01,(wchar_t *)local_98,&DAT_00424f54,(param_1 & 0xffff) >> 8);
  iVar1 = **(int **)((int)this + 0x778);
  pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
  (**(code **)(iVar1 + 0x2c))(pwVar3);
  DuiLib::CDuiString::Format(this_02,(wchar_t *)local_98,&DAT_00424f54,param_1 >> 0x10 & 0xff);
  iVar1 = **(int **)((int)this + 0x77c);
  pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
  (**(code **)(iVar1 + 0x2c))(pwVar3);
  DuiLib::CDuiString::~CDuiString(local_98);
  ExceptionList = local_10;
  return;
}


