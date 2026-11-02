// Program: SM809 mouse Software.exe
// Function: FUN_00410020
// Entry: 00410020
// Body: 00410020 - 0041038b
// Signature: undefined FUN_00410020(void * this, int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_00410020(void *this,int param_1)

{
  int *piVar1;
  CDuiString *pCVar2;
  wchar_t *pwVar3;
  int iVar4;
  code *pcVar5;
  CDuiString in_stack_fffffdc4;
  CDuiString aCStack_239 [121];
  CDuiString local_1a4 [136];
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_004227d5;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  piVar1 = *(int **)(param_1 + 0x108);
  if (piVar1 == *(int **)((int)this + 0x3a4)) {
    ExceptionList = &local_10;
    (**(code **)(**(int **)((int)this + 0x3a4) + 0x28))();
    local_8 = 0;
    DuiLib::CDuiString::CDuiString(aCStack_239 + -3,local_98);
    FUN_00403f90(in_stack_fffffdc4);
    pCVar2 = (CDuiString *)(**(code **)(**(int **)((int)this + 0x3a4) + 0x28))();
    local_8._0_1_ = 1;
    pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(pCVar2);
    iVar4 = _wtoi(pwVar3);
    pcVar5 = ~CDuiString_exref;
    local_8 = (uint)local_8._1_3_ << 8;
    DuiLib::CDuiString::~CDuiString(local_11c);
    if (iVar4 < 0x8000) {
      if (iVar4 < -0x7fff) {
        (**(code **)(**(int **)((int)this + 0x3a4) + 0x2c))();
      }
    }
    else {
      (**(code **)(**(int **)((int)this + 0x3a4) + 0x2c))();
    }
  }
  else if (piVar1 == *(int **)((int)this + 0x3a8)) {
    ExceptionList = &local_10;
    (**(code **)(**(int **)((int)this + 0x3a8) + 0x28))();
    local_8 = 2;
    DuiLib::CDuiString::CDuiString(aCStack_239 + -3,local_98);
    FUN_00403f90(in_stack_fffffdc4);
    pCVar2 = (CDuiString *)(**(code **)(**(int **)((int)this + 0x3a8) + 0x28))();
    local_8._0_1_ = 3;
    pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(pCVar2);
    iVar4 = _wtoi(pwVar3);
    pcVar5 = ~CDuiString_exref;
    local_8 = CONCAT31(local_8._1_3_,2);
    DuiLib::CDuiString::~CDuiString(local_11c);
    if (iVar4 < 0x8000) {
      if (iVar4 < -0x7fff) {
        (**(code **)(**(int **)((int)this + 0x3a8) + 0x2c))();
      }
    }
    else {
      (**(code **)(**(int **)((int)this + 0x3a8) + 0x2c))();
    }
  }
  else if (piVar1 == *(int **)((int)this + 0x3ac)) {
    ExceptionList = &local_10;
    (**(code **)(**(int **)((int)this + 0x3ac) + 0x28))();
    local_8 = 4;
    DuiLib::CDuiString::CDuiString(aCStack_239 + -3,local_98);
    FUN_00403f90(in_stack_fffffdc4);
    pCVar2 = (CDuiString *)(**(code **)(**(int **)((int)this + 0x3ac) + 0x28))();
    local_8._0_1_ = 5;
    pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(pCVar2);
    iVar4 = _wtoi(pwVar3);
    pcVar5 = ~CDuiString_exref;
    local_8 = CONCAT31(local_8._1_3_,4);
    DuiLib::CDuiString::~CDuiString(local_11c);
    if (iVar4 < 0x8000) {
      if (iVar4 < -0x7fff) {
        (**(code **)(**(int **)((int)this + 0x3ac) + 0x2c))();
      }
    }
    else {
      (**(code **)(**(int **)((int)this + 0x3ac) + 0x2c))();
    }
  }
  else {
    if (piVar1 != *(int **)((int)this + 0x3b0)) {
      return;
    }
    ExceptionList = &local_10;
    (**(code **)(**(int **)((int)this + 0x3b0) + 0x28))();
    local_8 = 6;
    DuiLib::CDuiString::CDuiString(aCStack_239 + -3,local_11c);
    FUN_00403f90(in_stack_fffffdc4);
    pCVar2 = (CDuiString *)(**(code **)(**(int **)((int)this + 0x3b0) + 0x28))();
    local_8._0_1_ = 7;
    pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(pCVar2);
    iVar4 = _wtoi(pwVar3);
    pcVar5 = ~CDuiString_exref;
    local_8 = CONCAT31(local_8._1_3_,6);
    DuiLib::CDuiString::~CDuiString(local_1a4);
    if ((0x7fff < iVar4) || (iVar4 < -0x7fff)) {
      (**(code **)(**(int **)((int)this + 0x3b0) + 0x2c))();
    }
  }
  (*pcVar5)();
  ExceptionList = local_10;
  return;
}


