// Program: SM809 mouse Software.exe
// Function: FUN_00409360
// Entry: 00409360
// Body: 00409360 - 00409483
// Signature: undefined FUN_00409360(int param_1)


void __fastcall FUN_00409360(int param_1)

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
    pwVar3 = L"add_gun_dir_text";
LAB_004093da:
    DuiLib::CDuiString::operator=((CDuiString *)(param_1 + 0x768),pwVar3);
    pwVar3 = L"input_gun_dir_text";
  }
  else {
    if (iVar1 == 1) {
      pwVar3 = L"add_gun_text";
    }
    else {
      if (iVar1 == 2) {
        pwVar3 = L"rename_gun_dir_text";
        goto LAB_004093da;
      }
      if (iVar1 != 3) goto LAB_0040942c;
      pwVar3 = L"rename_gun_text";
    }
    DuiLib::CDuiString::operator=((CDuiString *)(param_1 + 0x768),pwVar3);
    pwVar3 = L"input_gun_text";
  }
  DuiLib::CDuiString::operator=((CDuiString *)(param_1 + 0x7ec),pwVar3);
LAB_0040942c:
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


