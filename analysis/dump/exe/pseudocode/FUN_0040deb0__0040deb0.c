// Program: SM809 mouse Software.exe
// Function: FUN_0040deb0
// Entry: 0040deb0
// Body: 0040deb0 - 0040e0b6
// Signature: undefined FUN_0040deb0(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_0040deb0(int param_1)

{
  CControlUI *pCVar1;
  wchar_t *pwVar2;
  CDuiString *extraout_ECX;
  CDuiString *this;
  int iVar3;
  CDuiString *local_9c;
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
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"brightness_ver");
  *(CControlUI **)(param_1 + 0x4c) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"breathing_ver");
  *(CControlUI **)(param_1 + 0x50) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"current_color_control");
  *(CControlUI **)(param_1 + 0x5c) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"select_color_Pallet");
  *(CControlUI **)(param_1 + 0x60) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"brightness_slider");
  *(CControlUI **)(param_1 + 0x54) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"frequency_slider");
  *(CControlUI **)(param_1 + 0x58) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),L"r_edit");
  *(CControlUI **)(param_1 + 100) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),L"g_edit");
  *(CControlUI **)(param_1 + 0x68) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),L"b_edit");
  *(CControlUI **)(param_1 + 0x6c) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"btn_fix_color");
  *(CControlUI **)(param_1 + 0x70) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),L"color_ver");
  *(CControlUI **)(param_1 + 0x9c) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),L"length_ver")
  ;
  *(CControlUI **)(param_1 + 0xa0) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"length_slider");
  *(CControlUI **)(param_1 + 0xa4) = pCVar1;
  DuiLib::CDuiString::CDuiString(local_98);
  local_8 = 0;
  iVar3 = 0;
  this = extraout_ECX;
  local_9c = (CDuiString *)(param_1 + 0x1c);
  do {
    iVar3 = iVar3 + 1;
    DuiLib::CDuiString::Format(this,(wchar_t *)local_98,L"light_mode_option_%d",iVar3);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar1 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *(CControlUI **)local_9c = pCVar1;
    this = local_9c + 4;
    local_9c = this;
  } while (iVar3 < 0xc);
  iVar3 = 0;
  local_9c = (CDuiString *)(param_1 + 0x74);
  do {
    iVar3 = iVar3 + 1;
    DuiLib::CDuiString::Format(this,(wchar_t *)local_98,L"btn_cycle_color_%d",iVar3);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar1 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *(CControlUI **)local_9c = pCVar1;
    this = local_9c + 4;
    local_9c = this;
  } while (iVar3 < 8);
  iVar3 = 0;
  local_9c = (CDuiString *)(param_1 + 0x94);
  do {
    iVar3 = iVar3 + 1;
    DuiLib::CDuiString::Format(this,(wchar_t *)local_98,L"option_color_mode_%d",iVar3);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar1 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *(CControlUI **)local_9c = pCVar1;
    this = local_9c + 4;
    local_9c = this;
  } while (iVar3 < 2);
  DuiLib::CDuiString::~CDuiString(local_98);
  ExceptionList = local_10;
  return;
}


