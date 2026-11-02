// Program: SM809 mouse Software.exe
// Function: FUN_00406880
// Entry: 00406880
// Body: 00406880 - 00406a36
// Signature: undefined FUN_00406880(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_00406880(int param_1)

{
  uint uVar1;
  wchar_t *pwVar2;
  CControlUI *pCVar3;
  CDuiString *extraout_ECX;
  CDuiString *this;
  int iVar4;
  CDuiString *local_9c;
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_004216e1;
  local_10 = ExceptionList;
  uVar1 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  local_14 = uVar1;
  DuiLib::CDuiString::CDuiString(local_98);
  local_8 = 0;
  iVar4 = 0;
  this = extraout_ECX;
  local_9c = (CDuiString *)(param_1 + 0x20);
  do {
    iVar4 = iVar4 + 1;
    DuiLib::CDuiString::Format(this,(wchar_t *)local_98,L"button%d_btn",iVar4,uVar1);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar3 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *(CControlUI **)local_9c = pCVar3;
    this = local_9c + 4;
    local_9c = this;
  } while (iVar4 < 0x40);
  iVar4 = 0;
  local_9c = (CDuiString *)(param_1 + 0x120);
  do {
    iVar4 = iVar4 + 1;
    DuiLib::CDuiString::Format(this,(wchar_t *)local_98,L"button_mode_option_%d",iVar4);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar3 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *(CControlUI **)local_9c = pCVar3;
    this = local_9c + 4;
    local_9c = this;
  } while (iVar4 < 2);
  iVar4 = 0;
  local_9c = (CDuiString *)(param_1 + 0x13c);
  do {
    iVar4 = iVar4 + 1;
    DuiLib::CDuiString::Format(this,(wchar_t *)local_98,L"control_button_pic_%d",iVar4);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar3 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *(CControlUI **)local_9c = pCVar3;
    this = local_9c + 4;
    local_9c = this;
  } while (iVar4 < 0x20);
  pCVar3 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"office_mode_left");
  *(CControlUI **)(param_1 + 0x128) = pCVar3;
  pCVar3 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"office_mode_right");
  *(CControlUI **)(param_1 + 300) = pCVar3;
  pCVar3 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"game_mode_left");
  *(CControlUI **)(param_1 + 0x130) = pCVar3;
  pCVar3 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"game_mode_right");
  *(CControlUI **)(param_1 + 0x134) = pCVar3;
  pCVar3 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"ver_mouse_pic");
  *(CControlUI **)(param_1 + 0x138) = pCVar3;
  pCVar3 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"control_button_pic_0");
  *(CControlUI **)(param_1 + 0x1bc) = pCVar3;
  DuiLib::CDuiString::~CDuiString(local_98);
  ExceptionList = local_10;
  return;
}


