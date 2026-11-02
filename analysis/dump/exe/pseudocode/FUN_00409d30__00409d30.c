// Program: SM809 mouse Software.exe
// Function: FUN_00409d30
// Entry: 00409d30
// Body: 00409d30 - 00409e7c
// Signature: undefined FUN_00409d30(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_00409d30(int param_1)

{
  int iVar1;
  CControlUI *pCVar2;
  wchar_t *pwVar3;
  CDuiString *this;
  CDuiString *this_00;
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_004216e1;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  pCVar2 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(param_1 + 0x30),L"ok_btn");
  *(CControlUI **)(param_1 + 0x764) = pCVar2;
  pCVar2 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(param_1 + 0x30),L"cancel_btn");
  *(CControlUI **)(param_1 + 0x768) = pCVar2;
  pCVar2 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(param_1 + 0x30),L"exit_btn");
  *(CControlUI **)(param_1 + 0x76c) = pCVar2;
  pCVar2 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(param_1 + 0x30),L"edit_time");
  *(CControlUI **)(param_1 + 0x770) = pCVar2;
  pCVar2 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(param_1 + 0x30),L"edit_delay");
  *(CControlUI **)(param_1 + 0x774) = pCVar2;
  DuiLib::CDuiString::CDuiString(local_98);
  local_8 = 0;
  DuiLib::CDuiString::Format
            (this,(wchar_t *)local_98,&DAT_00424f54,*(undefined4 *)(param_1 + 0x77c));
  iVar1 = **(int **)(param_1 + 0x770);
  pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
  (**(code **)(iVar1 + 0x2c))(pwVar3);
  DuiLib::CDuiString::Format
            (this_00,(wchar_t *)local_98,&DAT_00424f54,*(undefined4 *)(param_1 + 0x780));
  iVar1 = **(int **)(param_1 + 0x774);
  pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
  (**(code **)(iVar1 + 0x2c))(pwVar3);
  DuiLib::CDuiString::~CDuiString(local_98);
  ExceptionList = local_10;
  return;
}


