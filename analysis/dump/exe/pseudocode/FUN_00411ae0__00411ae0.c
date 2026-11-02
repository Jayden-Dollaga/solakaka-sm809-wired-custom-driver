// Program: SM809 mouse Software.exe
// Function: FUN_00411ae0
// Entry: 00411ae0
// Body: 00411ae0 - 00411bbe
// Signature: undefined FUN_00411ae0(void * this, int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_00411ae0(void *this,int param_1)

{
  int iVar1;
  uint uVar2;
  CDuiString *pCVar3;
  CContainerUI *this_00;
  CControlUI *pCVar4;
  wchar_t *pwVar5;
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00422a3d;
  local_10 = ExceptionList;
  uVar2 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  local_14 = uVar2;
  DuiLib::CDuiString::CDuiString(local_98);
  local_8 = 0;
  pCVar3 = FUN_00402370(local_11c,(uint)*(byte *)((int)this + param_1 * 0x10 + 0x25));
  local_8._0_1_ = 1;
  DuiLib::CDuiString::operator=(local_98,pCVar3);
  local_8 = (uint)local_8._1_3_ << 8;
  DuiLib::CDuiString::~CDuiString(local_11c);
  this_00 = (CContainerUI *)
            (*(code *)**(undefined4 **)(*(int *)((int)this + 0x360) + 0x558))(param_1,uVar2);
  if (this_00 != (CContainerUI *)0x0) {
    pCVar4 = DuiLib::CContainerUI::FindSubControl(this_00,L"key");
    if (pCVar4 != (CControlUI *)0x0) {
      iVar1 = *(int *)pCVar4;
      pwVar5 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
      (**(code **)(iVar1 + 0x2c))(pwVar5);
    }
  }
  DuiLib::CDuiString::~CDuiString(local_98);
  ExceptionList = local_10;
  return;
}


