// Program: SM809 mouse Software.exe
// Function: FUN_00409e80
// Entry: 00409e80
// Body: 00409e80 - 00409feb
// Signature: undefined FUN_00409e80(void * this, CDuiString * param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_00409e80(void *this,CDuiString *param_1)

{
  bool bVar1;
  uint uVar2;
  wchar_t *pwVar3;
  int iVar4;
  CDuiString *this_00;
  undefined *puVar5;
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00421b3d;
  local_10 = ExceptionList;
  uVar2 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  local_14 = uVar2;
  bVar1 = DuiLib::CDuiString::operator==(param_1,L"click");
  if (bVar1) {
    (**(code **)(*(int *)((int)this + -0x20) + 0x20))(param_1);
    ExceptionList = local_10;
    return;
  }
  bVar1 = DuiLib::CDuiString::operator==(param_1,L"killfocus");
  if (!bVar1) {
    ExceptionList = local_10;
    return;
  }
  if (*(int **)(param_1 + 0x108) != *(int **)((int)this + 0x750)) {
    if (*(int **)(param_1 + 0x108) != *(int **)((int)this + 0x754)) {
      ExceptionList = local_10;
      return;
    }
    (**(code **)(**(int **)((int)this + 0x754) + 0x28))(local_11c,uVar2);
    local_8 = 1;
    pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_11c);
    iVar4 = _wtoi(pwVar3);
    if (iVar4 < 2) {
      iVar4 = 1;
      puVar5 = &DAT_00427820;
LAB_00409fb2:
      (**(code **)(**(int **)((int)this + 0x754) + 0x2c))(puVar5);
    }
    else if (0xfe < iVar4) {
      iVar4 = 0xff;
      puVar5 = &DAT_00427818;
      goto LAB_00409fb2;
    }
    *(int *)((int)this + 0x760) = iVar4;
    this_00 = local_11c;
    goto LAB_00409fc9;
  }
  (**(code **)(**(int **)((int)this + 0x750) + 0x28))(local_98);
  local_8 = 0;
  pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
  iVar4 = _wtoi(pwVar3);
  if (iVar4 < 1) {
    iVar4 = 0;
    puVar5 = &DAT_00427814;
LAB_00409f41:
    (**(code **)(**(int **)((int)this + 0x750) + 0x2c))(puVar5);
  }
  else if (0xfe < iVar4) {
    iVar4 = 0xff;
    puVar5 = &DAT_00427818;
    goto LAB_00409f41;
  }
  *(int *)((int)this + 0x75c) = iVar4;
  this_00 = local_98;
LAB_00409fc9:
  DuiLib::CDuiString::~CDuiString(this_00);
  ExceptionList = local_10;
  return;
}


