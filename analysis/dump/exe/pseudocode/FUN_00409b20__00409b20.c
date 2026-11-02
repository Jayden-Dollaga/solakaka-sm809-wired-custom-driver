// Program: SM809 mouse Software.exe
// Function: FUN_00409b20
// Entry: 00409b20
// Body: 00409b20 - 00409c43
// Signature: undefined FUN_00409b20(int param_1)


void __fastcall FUN_00409b20(int param_1)

{
  int iVar1;
  CControlUI *pCVar2;
  wchar_t *pwVar3;
  
  pCVar2 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(param_1 + 0x30),L"ok_btn");
  *(CControlUI **)(param_1 + 0x980) = pCVar2;
  pCVar2 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(param_1 + 0x30),L"cancel_btn");
  *(CControlUI **)(param_1 + 0x984) = pCVar2;
  pCVar2 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(param_1 + 0x30),L"exit_btn");
  *(CControlUI **)(param_1 + 0x988) = pCVar2;
  pCVar2 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(param_1 + 0x30),L"label_title");
  *(CControlUI **)(param_1 + 0x98c) = pCVar2;
  pCVar2 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(param_1 + 0x30),L"label_string")
  ;
  *(CControlUI **)(param_1 + 0x990) = pCVar2;
  pCVar2 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(param_1 + 0x30),L"edit_name");
  *(CControlUI **)(param_1 + 0x994) = pCVar2;
  iVar1 = *(int *)(param_1 + 0x97c);
  if (iVar1 == 0) {
    pwVar3 = L"add_macro_dir_text";
LAB_00409b9a:
    DuiLib::CDuiString::operator=((CDuiString *)(param_1 + 0x768),pwVar3);
    pwVar3 = L"input_macro_dir_text";
  }
  else {
    if (iVar1 == 1) {
      pwVar3 = L"add_macro_text";
    }
    else {
      if (iVar1 == 2) {
        pwVar3 = L"rename_macro_dir_text";
        goto LAB_00409b9a;
      }
      if (iVar1 != 3) goto LAB_00409bec;
      pwVar3 = L"rename_macro_text";
    }
    DuiLib::CDuiString::operator=((CDuiString *)(param_1 + 0x768),pwVar3);
    pwVar3 = L"input_macro_text";
  }
  DuiLib::CDuiString::operator=((CDuiString *)(param_1 + 0x7ec),pwVar3);
LAB_00409bec:
  iVar1 = **(int **)(param_1 + 0x98c);
  pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_((CDuiString *)(param_1 + 0x768));
  (**(code **)(iVar1 + 0x2c))(pwVar3);
  iVar1 = **(int **)(param_1 + 0x990);
  pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_((CDuiString *)(param_1 + 0x7ec));
  (**(code **)(iVar1 + 0x2c))(pwVar3);
  iVar1 = **(int **)(param_1 + 0x994);
  pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_((CDuiString *)(param_1 + 0x8f8));
  (**(code **)(iVar1 + 0x2c))(pwVar3);
  return;
}


