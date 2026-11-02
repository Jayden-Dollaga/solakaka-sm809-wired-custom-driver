// Program: SM809 mouse Software.exe
// Function: FUN_0040aea0
// Entry: 0040aea0
// Body: 0040aea0 - 0040b07a
// Signature: undefined FUN_0040aea0(void * this, int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_0040aea0(void *this,int param_1)

{
  int *piVar1;
  CDuiString *pCVar2;
  wchar_t *pwVar3;
  int iVar4;
  int iVar5;
  CDuiString in_stack_fffffdc4;
  CDuiString aCStack_239 [129];
  CDuiString local_1a4 [136];
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00421df5;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  iVar5 = 0;
  piVar1 = (int *)((int)this + 0x3a8);
  do {
    if (*(int **)(param_1 + 0x108) == (int *)piVar1[0x5a]) {
      ExceptionList = &local_10;
      (**(code **)(*(int *)piVar1[0x5a] + 0x28))();
      local_8 = 0;
      DuiLib::CDuiString::CDuiString(aCStack_239 + -3,local_11c);
      FUN_00403f90(in_stack_fffffdc4);
      pCVar2 = (CDuiString *)(**(code **)(**(int **)((int)this + iVar5 * 4 + 0x510) + 0x28))();
      local_8._0_1_ = 1;
      pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(pCVar2);
      iVar4 = _wtoi(pwVar3);
      local_8 = (uint)local_8._1_3_ << 8;
      DuiLib::CDuiString::~CDuiString(local_1a4);
      if ((0x7f < iVar4) || (iVar4 < -0x7f)) {
        (**(code **)(**(int **)((int)this + iVar5 * 4 + 0x510) + 0x2c))();
      }
      pCVar2 = local_11c;
LAB_0040b057:
      DuiLib::CDuiString::~CDuiString(pCVar2);
      ExceptionList = local_10;
      return;
    }
    if (*(int **)(param_1 + 0x108) == (int *)*piVar1) {
      ExceptionList = &local_10;
      (**(code **)(*(int *)*piVar1 + 0x28))();
      local_8 = 2;
      DuiLib::CDuiString::CDuiString(aCStack_239 + -3,local_98);
      FUN_00403f90(in_stack_fffffdc4);
      pCVar2 = (CDuiString *)(**(code **)(**(int **)((int)this + iVar5 * 4 + 0x3a8) + 0x28))();
      local_8._0_1_ = 3;
      pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(pCVar2);
      iVar4 = _wtoi(pwVar3);
      local_8 = CONCAT31(local_8._1_3_,2);
      DuiLib::CDuiString::~CDuiString(local_1a4);
      if (iVar4 < 0x80) {
        if (iVar4 < -0x7f) {
          (**(code **)(**(int **)((int)this + iVar5 * 4 + 0x3a8) + 0x2c))();
        }
        pCVar2 = local_98;
      }
      else {
        (**(code **)(**(int **)((int)this + iVar5 * 4 + 0x3a8) + 0x2c))();
        pCVar2 = local_98;
      }
      goto LAB_0040b057;
    }
    iVar5 = iVar5 + 1;
    piVar1 = piVar1 + 1;
    if (0x1d < iVar5) {
      return;
    }
  } while( true );
}


