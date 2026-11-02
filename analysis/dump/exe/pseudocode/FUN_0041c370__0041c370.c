// Program: SM809 mouse Software.exe
// Function: FUN_0041c370
// Entry: 0041c370
// Body: 0041c370 - 0041c408
// Signature: undefined FUN_0041c370(int param_1)


void __fastcall FUN_0041c370(int param_1)

{
  int iVar1;
  CControlUI *pCVar2;
  wchar_t *pwVar3;
  
  pCVar2 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(param_1 + 0x30),L"ok_btn");
  *(CControlUI **)(param_1 + 0x764) = pCVar2;
  pCVar2 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(param_1 + 0x30),L"cancel_btn");
  *(CControlUI **)(param_1 + 0x768) = pCVar2;
  pCVar2 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(param_1 + 0x30),L"exit_btn");
  *(CControlUI **)(param_1 + 0x76c) = pCVar2;
  pCVar2 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(param_1 + 0x30),L"label_title");
  *(CControlUI **)(param_1 + 0x770) = pCVar2;
  pCVar2 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(param_1 + 0x30),L"label_string")
  ;
  *(CControlUI **)(param_1 + 0x774) = pCVar2;
  iVar1 = **(int **)(param_1 + 0x770);
  pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_((CDuiString *)(param_1 + 0x77c));
  (**(code **)(iVar1 + 0x2c))(pwVar3);
  iVar1 = **(int **)(param_1 + 0x774);
  pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_((CDuiString *)(param_1 + 0x800));
  (**(code **)(iVar1 + 0x2c))(pwVar3);
  return;
}


