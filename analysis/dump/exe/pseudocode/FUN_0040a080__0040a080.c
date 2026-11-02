// Program: SM809 mouse Software.exe
// Function: FUN_0040a080
// Entry: 0040a080
// Body: 0040a080 - 0040a3c0
// Signature: undefined FUN_0040a080(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_0040a080(int param_1)

{
  CControlUI *pCVar1;
  wchar_t *pwVar2;
  CDuiString *extraout_ECX;
  CDuiString *this;
  int iVar3;
  int local_a0;
  CDuiString *local_9c;
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00421c31;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),L"gun_combo");
  *(CControlUI **)(param_1 + 0x1b0) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"btn_add_gun");
  *(CControlUI **)(param_1 + 0x1b4) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"btn_delete_gun");
  *(CControlUI **)(param_1 + 0x1b8) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"btn_menu_gun");
  *(CControlUI **)(param_1 + 0x1bc) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"edit_gun_name");
  *(CControlUI **)(param_1 + 0x1c0) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"zidan_combo");
  *(CControlUI **)(param_1 + 0x1c4) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"btn_add_gun_floder");
  *(CControlUI **)(param_1 + 0x678) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"btn_delete_gun_floder");
  *(CControlUI **)(param_1 + 0x67c) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"btn_menu_gun_floder");
  *(CControlUI **)(param_1 + 0x680) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),L"gun_list");
  *(CControlUI **)(param_1 + 0x684) = pCVar1;
  DuiLib::CDuiString::CDuiString(local_98);
  local_8 = 0;
  iVar3 = 1;
  local_a0 = 0x1e;
  this = extraout_ECX;
  local_9c = (CDuiString *)(param_1 + 0x240);
  do {
    DuiLib::CDuiString::Format(this,(wchar_t *)local_98,L"ver_zidan_num_%d",iVar3);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar1 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *(CControlUI **)(local_9c + -0x78) = pCVar1;
    DuiLib::CDuiString::Format(local_9c,(wchar_t *)local_98,L"edit_zidan_delay_%d",iVar3);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar1 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *(CControlUI **)local_9c = pCVar1;
    DuiLib::CDuiString::Format(local_9c,(wchar_t *)local_98,L"edit_zidan_y_%d",iVar3);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar1 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *(CControlUI **)(local_9c + 0x168) = pCVar1;
    DuiLib::CDuiString::Format(local_9c,(wchar_t *)local_98,L"edit_zidan_x_%d",iVar3);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar1 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *(CControlUI **)(local_9c + 0x2d0) = pCVar1;
    DuiLib::CDuiString::Format(local_9c,(wchar_t *)local_98,L"zidan_delay_up_btn_%d",iVar3);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar1 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *(CControlUI **)(local_9c + 0x78) = pCVar1;
    DuiLib::CDuiString::Format(local_9c,(wchar_t *)local_98,L"zidan_delay_down_btn_%d",iVar3);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar1 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *(CControlUI **)(local_9c + 0xf0) = pCVar1;
    DuiLib::CDuiString::Format(local_9c,(wchar_t *)local_98,L"zidan_y_up_btn_%d",iVar3);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar1 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *(CControlUI **)(local_9c + 0x1e0) = pCVar1;
    DuiLib::CDuiString::Format(local_9c,(wchar_t *)local_98,L"zidan_y_down_btn_%d",iVar3);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar1 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *(CControlUI **)(local_9c + 600) = pCVar1;
    DuiLib::CDuiString::Format(local_9c,(wchar_t *)local_98,L"zidan_x_down_btn_%d",iVar3);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar1 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *(CControlUI **)(local_9c + 0x348) = pCVar1;
    DuiLib::CDuiString::Format(local_9c,(wchar_t *)local_98,L"zidan_x_up_btn_%d",iVar3);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar1 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    iVar3 = iVar3 + 1;
    *(CControlUI **)(local_9c + 0x3c0) = pCVar1;
    this = local_9c + 4;
    local_a0 = local_a0 + -1;
    local_9c = this;
  } while (local_a0 != 0);
  DuiLib::CDuiString::~CDuiString(local_98);
  ExceptionList = local_10;
  return;
}


