// Program: SM809 mouse Software.exe
// Function: FUN_0040ee10
// Entry: 0040ee10
// Body: 0040ee10 - 0040f1d2
// Signature: undefined FUN_0040ee10(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_0040ee10(int param_1)

{
  CControlUI *pCVar1;
  wchar_t *pwVar2;
  CDuiString *pCVar3;
  HMODULE hModule;
  DWORD DVar4;
  FARPROC pFVar5;
  BOOL BVar6;
  CDuiString *extraout_ECX;
  CDuiString *extraout_ECX_00;
  CDuiString *this;
  undefined4 *puVar7;
  int iVar8;
  CDuiString local_224 [132];
  CDuiString local_1a0 [132];
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00422671;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"macro_combo");
  *(CControlUI **)(param_1 + 0x338) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"btn_add_macro");
  *(CControlUI **)(param_1 + 0x33c) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"btn_delete_macro");
  *(CControlUI **)(param_1 + 0x340) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"btn_menu_macro");
  *(CControlUI **)(param_1 + 0x344) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"edit_macro_name");
  *(CControlUI **)(param_1 + 0x348) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"edit_default_delay");
  *(CControlUI **)(param_1 + 0x358) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),L"btn_record")
  ;
  *(CControlUI **)(param_1 + 0x35c) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"macro_action_list");
  *(CControlUI **)(param_1 + 0x360) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"btn_macro_move_up");
  *(CControlUI **)(param_1 + 0x364) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"btn_macro_move_down");
  *(CControlUI **)(param_1 + 0x368) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"btn_macro_action_delete");
  *(CControlUI **)(param_1 + 0x36c) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"btn_macro_clear_all");
  *(CControlUI **)(param_1 + 0x370) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"edit_macro_action");
  *(CControlUI **)(param_1 + 0x374) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"edit_macro_delay");
  *(CControlUI **)(param_1 + 0x378) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"macro_key_hor");
  *(CControlUI **)(param_1 + 0x37c) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"macro_delay_hor");
  *(CControlUI **)(param_1 + 0x380) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"macro_mouse_action_combo");
  *(CControlUI **)(param_1 + 900) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"edit_loop_time");
  *(CControlUI **)(param_1 + 0x388) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"btn_add_macro_floder");
  *(CControlUI **)(param_1 + 0x38c) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"btn_delete_macro_floder");
  *(CControlUI **)(param_1 + 0x390) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"btn_menu_macro_floder");
  *(CControlUI **)(param_1 + 0x394) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),L"macro_list")
  ;
  *(CControlUI **)(param_1 + 0x398) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"btn_insert_move");
  *(CControlUI **)(param_1 + 0x39c) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"macro_mouse_move_hor");
  *(CControlUI **)(param_1 + 0x3a0) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"edit_macro_action_x");
  *(CControlUI **)(param_1 + 0x3a4) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"edit_macro_action_y");
  *(CControlUI **)(param_1 + 0x3a8) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"edit_insert_x");
  *(CControlUI **)(param_1 + 0x3ac) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"edit_insert_y");
  *(CControlUI **)(param_1 + 0x3b0) = pCVar1;
  DuiLib::CDuiString::CDuiString(local_1a0);
  local_8 = 0;
  puVar7 = (undefined4 *)(param_1 + 0x34c);
  iVar8 = 0;
  pCVar3 = extraout_ECX;
  do {
    iVar8 = iVar8 + 1;
    DuiLib::CDuiString::Format(pCVar3,(wchar_t *)local_1a0,L"macro_delay_option_%d",iVar8);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_1a0);
    pCVar1 = DuiLib::CPaintManagerUI::FindControl(*(CPaintManagerUI **)(param_1 + 0x10),pwVar2);
    *puVar7 = pCVar1;
    puVar7 = puVar7 + 1;
    pCVar3 = extraout_ECX_00;
  } while (iVar8 < 3);
  DuiLib::CDuiString::CDuiString(local_98);
  local_8._0_1_ = 1;
  pCVar3 = FUN_00401e90(local_224);
  local_8._0_1_ = 2;
  pCVar3 = (CDuiString *)DuiLib::CDuiString::operator+(pCVar3,(wchar_t *)local_11c);
  local_8._0_1_ = 3;
  DuiLib::CDuiString::operator=(local_98,pCVar3);
  DuiLib::CDuiString::~CDuiString(local_11c);
  local_8._0_1_ = 1;
  DuiLib::CDuiString::~CDuiString(local_224);
  pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
  hModule = LoadLibraryW(pwVar2);
  *(HMODULE *)(param_1 + 0x2f0) = hModule;
  if (hModule == (HMODULE)0x0) {
    DVar4 = GetLastError();
    DuiLib::CDuiString::CDuiString(local_11c);
    local_8._0_1_ = 4;
    DuiLib::CDuiString::Format(this,(wchar_t *)local_11c,L"GetError:%d\n",DVar4);
    DuiLib::CDuiString::~CDuiString(local_11c);
  }
  else {
    pFVar5 = GetProcAddress(hModule,"installmousehook");
    *(FARPROC *)(param_1 + 0x318) = pFVar5;
    pFVar5 = GetProcAddress(*(HMODULE *)(param_1 + 0x2f0),"removemousehook");
    *(FARPROC *)(param_1 + 0x31c) = pFVar5;
    pFVar5 = GetProcAddress(*(HMODULE *)(param_1 + 0x2f0),"enablemousehook");
    *(FARPROC *)(param_1 + 800) = pFVar5;
    pFVar5 = GetProcAddress(*(HMODULE *)(param_1 + 0x2f0),"installhook");
    *(FARPROC *)(param_1 + 0x324) = pFVar5;
    pFVar5 = GetProcAddress(*(HMODULE *)(param_1 + 0x2f0),"removehook");
    *(FARPROC *)(param_1 + 0x328) = pFVar5;
    pFVar5 = GetProcAddress(*(HMODULE *)(param_1 + 0x2f0),"enablehook");
    *(FARPROC *)(param_1 + 0x32c) = pFVar5;
    pFVar5 = GetProcAddress(*(HMODULE *)(param_1 + 0x2f0),"MouseMoveHook");
    *(FARPROC *)(param_1 + 0x334) = pFVar5;
  }
  DuiLib::CDuiString::~CDuiString(local_98);
  BVar6 = QueryPerformanceFrequency((LARGE_INTEGER *)(param_1 + 0x2d0));
  *(BOOL *)(param_1 + 0x2ec) = BVar6;
  DuiLib::CDuiString::~CDuiString(local_1a0);
  ExceptionList = local_10;
  return;
}


