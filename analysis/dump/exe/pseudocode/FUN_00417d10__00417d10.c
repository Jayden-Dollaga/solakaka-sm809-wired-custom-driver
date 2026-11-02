// Program: SM809 mouse Software.exe
// Function: FUN_00417d10
// Entry: 00417d10
// Body: 00417d10 - 00417eb4
// Signature: undefined FUN_00417d10(void * this, int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_00417d10(void *this,int param_1)

{
  CDuiString *pCVar1;
  wchar_t *pwVar2;
  int iVar3;
  CDuiString in_stack_fffffdc8;
  CDuiString aCStack_235 [117];
  CDuiString local_1a4 [132];
  int *local_120;
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_004234d9;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  if (*(int *)(param_1 + 0x108) == *(int *)((int)this + 0x170c)) {
    DuiLib::CDuiString::CDuiString(local_98);
    local_8 = 0;
    DuiLib::CDuiString::CDuiString(local_11c);
    local_8._0_1_ = 1;
    pCVar1 = (CDuiString *)(**(code **)(**(int **)((int)this + 0x170c) + 0x28))();
    local_8._0_1_ = 2;
    DuiLib::CDuiString::operator=(local_98,pCVar1);
    local_8 = CONCAT31(local_8._1_3_,1);
    DuiLib::CDuiString::~CDuiString(local_1a4);
    DuiLib::CDuiString::operator=(local_11c,DAT_00432aa0);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_11c);
    iVar3 = DuiLib::CDuiString::CompareNoCase(local_98,pwVar2);
    if (iVar3 != 0) {
      DuiLib::CDuiString::CDuiString(aCStack_235 + -3,local_98);
      iVar3 = FUN_004039e0(in_stack_fffffdc8);
      if (iVar3 == 0) {
        pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
        wcscpy_s(DAT_00432aa0,0x32,pwVar2);
        local_120 = (int *)(*(code *)**(undefined4 **)(*(int *)((int)this + 0x16fc) + 0x558))();
        if (local_120 != (int *)0x0) {
          iVar3 = *local_120;
          DuiLib::CDuiString::GetData(local_98);
          (**(code **)(iVar3 + 0x2c))();
          DuiLib::CControlUI::Invalidate(*(CControlUI **)((int)this + 0x16fc));
        }
        FUN_004035a0();
      }
      else {
        iVar3 = **(int **)((int)this + 0x170c);
        DuiLib::CDuiString::operator_wchar_t_const_(local_11c);
        (**(code **)(iVar3 + 0x2c))();
      }
    }
    DuiLib::CDuiString::~CDuiString(local_11c);
    DuiLib::CDuiString::~CDuiString(local_98);
  }
  ExceptionList = local_10;
  return;
}


