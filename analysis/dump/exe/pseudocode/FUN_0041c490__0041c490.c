// Program: SM809 mouse Software.exe
// Function: FUN_0041c490
// Entry: 0041c490
// Body: 0041c490 - 0041c7ef
// Signature: undefined FUN_0041c490(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_0041c490(int param_1)

{
  uint uVar1;
  wchar_t *pwVar2;
  CControlUI *pCVar3;
  CDuiString *extraout_ECX;
  CDuiString *this;
  CDuiString *extraout_ECX_00;
  undefined4 *puVar4;
  int iVar5;
  int local_a4;
  int local_a0;
  CDuiString *local_9c;
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00423861;
  local_10 = ExceptionList;
  uVar1 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  local_14 = uVar1;
  DuiLib::CDuiString::CDuiString(local_98);
  local_8 = 0;
  puVar4 = (undefined4 *)(param_1 + 0x18);
  iVar5 = 0;
  this = extraout_ECX;
  do {
    iVar5 = iVar5 + 1;
    DuiLib::CDuiString::Format(this,(wchar_t *)local_98,L"prate_%d_option",iVar5,uVar1);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar3 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *puVar4 = pCVar3;
    puVar4 = puVar4 + 1;
    this = extraout_ECX_00;
  } while (iVar5 < 4);
  local_9c = (CDuiString *)(param_1 + 0x48);
  local_a0 = 1;
  local_a4 = 8;
  do {
    DuiLib::CDuiString::Format(local_9c,(wchar_t *)local_98,L"mouse_dpi_btn_%d",local_a0);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar3 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *(CControlUI **)(local_9c + -0x20) = pCVar3;
    DuiLib::CDuiString::Format(local_9c,(wchar_t *)local_98,L"mouse_dpi_value_%d",local_a0);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar3 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *(CControlUI **)local_9c = pCVar3;
    DuiLib::CDuiString::Format(local_9c,(wchar_t *)local_98,L"mouse_dpi%d_slider",local_a0);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar3 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *(CControlUI **)(local_9c + 0x20) = pCVar3;
    DuiLib::CDuiString::Format(local_9c,(wchar_t *)local_98,L"dpi_setting_ver_%d",local_a0);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar3 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *(CControlUI **)(local_9c + 0x40) = pCVar3;
    DuiLib::CDuiString::Format(local_9c,(wchar_t *)local_98,L"label_dpi_left_%d",local_a0);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar3 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *(CControlUI **)(local_9c + 0x60) = pCVar3;
    DuiLib::CDuiString::Format(local_9c,(wchar_t *)local_98,L"label_dpi_right_%d",local_a0);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar3 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *(CControlUI **)(local_9c + 0x80) = pCVar3;
    DuiLib::CDuiString::Format(local_9c,(wchar_t *)local_98,L"mouse_dpi_color%d",local_a0);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar3 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *(CControlUI **)(local_9c + 0xa0) = pCVar3;
    local_9c = local_9c + 4;
    local_a0 = local_a0 + 1;
    local_a4 = local_a4 + -1;
  } while (local_a4 != 0);
  pCVar3 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"max_dpi_combo");
  *(CControlUI **)(param_1 + 0x134) = pCVar3;
  pCVar3 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"mouse_move_speed_slider");
  *(CControlUI **)(param_1 + 0x108) = pCVar3;
  pCVar3 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"scroll_speed_slider");
  *(CControlUI **)(param_1 + 0x10c) = pCVar3;
  pCVar3 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"double_click_speed_slider");
  *(CControlUI **)(param_1 + 0x110) = pCVar3;
  pCVar3 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"enhance_pointer_checkbox");
  *(CControlUI **)(param_1 + 0x114) = pCVar3;
  pCVar3 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"one_page_checkbox");
  *(CControlUI **)(param_1 + 0x118) = pCVar3;
  pCVar3 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"lift_of_distance_slider");
  *(CControlUI **)(param_1 + 0x11c) = pCVar3;
  pCVar3 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"lift_of_distance_ver");
  *(CControlUI **)(param_1 + 0x120) = pCVar3;
  pCVar3 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"distance_checkbox");
  *(CControlUI **)(param_1 + 0x124) = pCVar3;
  pCVar3 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"distance_slider_ver");
  *(CControlUI **)(param_1 + 0x128) = pCVar3;
  pCVar3 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"key_response_slider");
  *(CControlUI **)(param_1 + 300) = pCVar3;
  pCVar3 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"label_key_respsonse");
  *(CControlUI **)(param_1 + 0x130) = pCVar3;
  FUN_0041d110(param_1);
  (**(code **)(**(int **)(param_1 + 0x120) + 0xf8))(DAT_00432acc != 0);
  DuiLib::CProgressUI::SetMinValue(*(CProgressUI **)(param_1 + 0x11c),DAT_00432ad4);
  DuiLib::CProgressUI::SetMaxValue(*(CProgressUI **)(param_1 + 0x11c),DAT_00432ad0);
  DuiLib::CDuiString::~CDuiString(local_98);
  ExceptionList = local_10;
  return;
}


