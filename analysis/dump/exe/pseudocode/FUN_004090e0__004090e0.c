// Program: SM809 mouse Software.exe
// Function: FUN_004090e0
// Entry: 004090e0
// Body: 004090e0 - 00409131
// Signature: undefined FUN_004090e0(int param_1)


void __fastcall FUN_004090e0(int param_1)

{
  int iVar1;
  CControlUI *pCVar2;
  wchar_t *pwVar3;
  
  pCVar2 = DuiLib::CPaintManagerUI::FindControl
                     ((CPaintManagerUI *)(param_1 + 0x30),L"dpi_value_label");
  *(CControlUI **)(param_1 + 0x768) = pCVar2;
  if (pCVar2 != (CControlUI *)0x0) {
    iVar1 = *(int *)pCVar2;
    pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_((CDuiString *)(param_1 + 0x76c));
    (**(code **)(iVar1 + 0x2c))(pwVar3);
    SetWindowPos(*(HWND *)(param_1 + 4),(HWND)0xffffffff,0x14,0x14,0x96,0x96,0x14);
  }
  return;
}


