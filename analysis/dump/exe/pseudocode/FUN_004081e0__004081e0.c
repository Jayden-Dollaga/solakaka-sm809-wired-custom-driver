// Program: SM809 mouse Software.exe
// Function: FUN_004081e0
// Entry: 004081e0
// Body: 004081e0 - 00408a57
// Signature: undefined FUN_004081e0(void * this, int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_004081e0(void *this,int param_1)

{
  undefined1 uVar1;
  byte bVar2;
  int iVar3;
  uint uVar4;
  CResourceManager *pCVar5;
  CDuiString *pCVar6;
  undefined4 uVar7;
  code *pcVar8;
  wchar_t *pwVar9;
  CDuiString local_3bc [132];
  CDuiString local_338 [132];
  CDuiString local_2b4 [132];
  undefined4 *local_230;
  wchar_t *local_22c;
  byte local_225;
  CDuiString local_224 [132];
  CDuiString local_1a0 [132];
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_004219f9;
  local_10 = ExceptionList;
  uVar4 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  local_22c = (wchar_t *)(DAT_00432aa0 + 0x150 + param_1 * 0x72c);
  uVar1 = *(undefined1 *)((int)local_22c + 0xc9);
  local_14 = uVar4;
  DuiLib::CDuiString::CDuiString(local_98);
  local_8 = 0;
  local_230 = (undefined4 *)((int)this + (param_1 + 8) * 4);
  (**(code **)(**(int **)((int)this + (param_1 + 8) * 4) + 0x34))(1,uVar4);
  switch(uVar1) {
  case 0:
    pwVar9 = L"button_off_text";
    break;
  default:
    pwVar9 = L"click_text";
    break;
  case 2:
    pwVar9 = L"menu_text";
    break;
  case 3:
    pwVar9 = L"scroll_text";
    break;
  case 4:
    pwVar9 = L"forward_text";
    break;
  case 5:
    pwVar9 = L"backward_text";
    break;
  case 6:
    pwVar9 = L"dpi_cycle_text";
    break;
  case 7:
    pwVar9 = L"dpi_up_text";
    break;
  case 8:
    pwVar9 = L"dpi_down_text";
    break;
  case 9:
    pwVar9 = L"double_click_text";
    break;
  case 10:
    pwVar9 = L"fire_click_text";
    break;
  case 0xb:
    pwVar9 = L"scroll_up_text";
    break;
  case 0xc:
    pwVar9 = L"scroll_down_text";
    break;
  case 0x12:
    pwVar9 = L"three_click_text";
    break;
  case 0x15:
    (**(code **)(**(int **)((int)this + param_1 * 4 + 0x20) + 0x34))(0);
    bVar2 = *(byte *)((int)local_22c + 0xdd);
    DuiLib::CDuiString::CDuiString(local_224);
    local_8._0_1_ = 1;
    DuiLib::CDuiString::CDuiString(local_1a0);
    local_8._0_1_ = 2;
    pCVar6 = FUN_00402370(local_11c,(uint)bVar2);
    local_8._0_1_ = 3;
    DuiLib::CDuiString::operator=(local_224,pCVar6);
    local_8._0_1_ = 2;
    DuiLib::CDuiString::~CDuiString(local_11c);
    pwVar9 = DuiLib::CDuiString::operator_wchar_t_const_(local_224);
    pCVar6 = local_11c;
    pCVar5 = DuiLib::CResourceManager::GetInstance();
    pCVar6 = (CDuiString *)DuiLib::CResourceManager::GetText(pCVar5,(wchar_t *)pCVar6,pwVar9);
    local_8._0_1_ = 4;
    DuiLib::CDuiString::operator=(local_224,pCVar6);
    local_8._0_1_ = 2;
    DuiLib::CDuiString::~CDuiString(local_11c);
    local_225 = (byte)local_22c[0x6e];
    if ((local_225 & 1) != 0) {
      pCVar6 = local_2b4;
      pwVar9 = L"ctrl_text";
      pCVar5 = DuiLib::CResourceManager::GetInstance();
      pCVar6 = (CDuiString *)DuiLib::CResourceManager::GetText(pCVar5,(wchar_t *)pCVar6,pwVar9);
      local_8._0_1_ = 5;
      pCVar6 = (CDuiString *)DuiLib::CDuiString::operator+(pCVar6,(wchar_t *)local_11c);
      local_8._0_1_ = 6;
      DuiLib::CDuiString::operator+=(local_1a0,pCVar6);
      DuiLib::CDuiString::~CDuiString(local_11c);
      local_8._0_1_ = 2;
      DuiLib::CDuiString::~CDuiString(local_2b4);
    }
    if ((local_225 & 2) != 0) {
      pCVar6 = local_11c;
      pwVar9 = L"shift_text";
      pCVar5 = DuiLib::CResourceManager::GetInstance();
      pCVar6 = (CDuiString *)DuiLib::CResourceManager::GetText(pCVar5,(wchar_t *)pCVar6,pwVar9);
      local_8._0_1_ = 7;
      pCVar6 = (CDuiString *)DuiLib::CDuiString::operator+(pCVar6,(wchar_t *)local_2b4);
      local_8._0_1_ = 8;
      DuiLib::CDuiString::operator+=(local_1a0,pCVar6);
      DuiLib::CDuiString::~CDuiString(local_2b4);
      local_8._0_1_ = 2;
      DuiLib::CDuiString::~CDuiString(local_11c);
    }
    if ((local_225 & 4) != 0) {
      pCVar6 = local_11c;
      pwVar9 = L"alt_text";
      pCVar5 = DuiLib::CResourceManager::GetInstance();
      pCVar6 = (CDuiString *)DuiLib::CResourceManager::GetText(pCVar5,(wchar_t *)pCVar6,pwVar9);
      local_8._0_1_ = 9;
      pCVar6 = (CDuiString *)DuiLib::CDuiString::operator+(pCVar6,(wchar_t *)local_2b4);
      local_8._0_1_ = 10;
      DuiLib::CDuiString::operator+=(local_1a0,pCVar6);
      DuiLib::CDuiString::~CDuiString(local_2b4);
      local_8._0_1_ = 2;
      DuiLib::CDuiString::~CDuiString(local_11c);
    }
    if ((local_225 & 8) != 0) {
      pCVar6 = local_11c;
      pwVar9 = L"win_text";
      pCVar5 = DuiLib::CResourceManager::GetInstance();
      pCVar6 = (CDuiString *)DuiLib::CResourceManager::GetText(pCVar5,(wchar_t *)pCVar6,pwVar9);
      local_8._0_1_ = 0xb;
      pCVar6 = (CDuiString *)DuiLib::CDuiString::operator+(pCVar6,(wchar_t *)local_2b4);
      local_8._0_1_ = 0xc;
      DuiLib::CDuiString::operator+=(local_1a0,pCVar6);
      DuiLib::CDuiString::~CDuiString(local_2b4);
      local_8._0_1_ = 2;
      DuiLib::CDuiString::~CDuiString(local_11c);
    }
    pCVar6 = (CDuiString *)DuiLib::CDuiString::operator+(local_1a0,local_2b4);
    local_8._0_1_ = 0xd;
    DuiLib::CDuiString::operator=(local_98,pCVar6);
    DuiLib::CDuiString::~CDuiString(local_2b4);
    DuiLib::CDuiString::~CDuiString(local_1a0);
    local_8 = (uint)local_8._1_3_ << 8;
    DuiLib::CDuiString::~CDuiString(local_224);
    goto LAB_00408a16;
  case 0x16:
    DuiLib::CDuiString::CDuiString(local_11c);
    local_8._0_1_ = 0xe;
    DuiLib::CDuiString::CDuiString(local_1a0);
    local_8._0_1_ = 0xf;
    DuiLib::CDuiString::CDuiString(local_224);
    pCVar6 = local_2b4;
    local_8._0_1_ = 0x10;
    pwVar9 = L"set_macro_text";
    pCVar5 = DuiLib::CResourceManager::GetInstance();
    pCVar6 = (CDuiString *)DuiLib::CResourceManager::GetText(pCVar5,(wchar_t *)pCVar6,pwVar9);
    local_8._0_1_ = 0x11;
    DuiLib::CDuiString::operator=(local_11c,pCVar6);
    local_8._0_1_ = 0x10;
    DuiLib::CDuiString::~CDuiString(local_2b4);
    DuiLib::CDuiString::operator=(local_1a0,local_22c);
    DuiLib::CDuiString::operator=(local_224,local_22c + 0x32);
    (**(code **)(*(int *)*local_230 + 0x34))(0);
    pCVar6 = (CDuiString *)DuiLib::CDuiString::operator+(local_11c,local_338);
    local_8._0_1_ = 0x12;
    pCVar6 = (CDuiString *)DuiLib::CDuiString::operator+(pCVar6,(wchar_t *)local_3bc);
    local_8._0_1_ = 0x13;
    pCVar6 = (CDuiString *)DuiLib::CDuiString::operator+(pCVar6,local_2b4);
    local_8._0_1_ = 0x14;
    DuiLib::CDuiString::operator=(local_98,pCVar6);
    DuiLib::CDuiString::~CDuiString(local_2b4);
    DuiLib::CDuiString::~CDuiString(local_3bc);
    DuiLib::CDuiString::~CDuiString(local_338);
    DuiLib::CDuiString::~CDuiString(local_224);
    DuiLib::CDuiString::~CDuiString(local_1a0);
    local_8 = (uint)local_8._1_3_ << 8;
    DuiLib::CDuiString::~CDuiString(local_11c);
    goto LAB_00408a16;
  case 0x19:
    pwVar9 = L"send_gun_text";
    break;
  case 0x1a:
    pwVar9 = L"mode_switch_text";
    break;
  case 0x20:
    pwVar9 = L"cut_text";
    break;
  case 0x21:
    pwVar9 = L"copy_text";
    break;
  case 0x22:
    pwVar9 = L"paste_text";
    break;
  case 0x23:
    pwVar9 = L"open_text";
    break;
  case 0x24:
    pwVar9 = L"save_text";
    break;
  case 0x25:
    pwVar9 = L"find_text";
    break;
  case 0x26:
    pwVar9 = L"redo_text";
    break;
  case 0x28:
    pwVar9 = L"select_all_text";
    break;
  case 0x29:
    pwVar9 = L"print_text";
    break;
  case 0x2a:
    pwVar9 = L"close_windows_text";
    break;
  case 0x2b:
    pwVar9 = L"swap_windows_text";
    break;
  case 0x2c:
    pwVar9 = L"show_desktop_text";
    break;
  case 0x2d:
    pwVar9 = L"run_command_text";
    break;
  case 0x2e:
    pwVar9 = L"lock_pc_text";
    break;
  case 0x2f:
    pwVar9 = L"new_text";
    break;
  case 0x32:
    pwVar9 = L"light_mode_switch_text";
    break;
  case 0x39:
    DuiLib::CDuiString::CDuiString(local_1a0);
    local_8._0_1_ = 0x15;
    DuiLib::CDuiString::CDuiString(local_224);
    local_8._0_1_ = 0x16;
    DuiLib::CDuiString::CDuiString(local_11c);
    pCVar6 = local_338;
    local_8._0_1_ = 0x17;
    pwVar9 = L"set_left_macro_text";
    pCVar5 = DuiLib::CResourceManager::GetInstance();
    pCVar6 = (CDuiString *)DuiLib::CResourceManager::GetText(pCVar5,(wchar_t *)pCVar6,pwVar9);
    pcVar8 = operator=_exref;
    local_8._0_1_ = 0x18;
    DuiLib::CDuiString::operator=(local_1a0,pCVar6);
    local_8._0_1_ = 0x17;
    DuiLib::CDuiString::~CDuiString(local_338);
    DuiLib::CDuiString::operator=(local_224,local_22c);
    DuiLib::CDuiString::operator=(local_11c,local_22c + 0x32);
    (**(code **)(*(int *)*local_230 + 0x34))(0);
    pCVar6 = (CDuiString *)DuiLib::CDuiString::operator+(local_1a0,local_2b4);
    local_8._0_1_ = 0x19;
    pCVar6 = (CDuiString *)DuiLib::CDuiString::operator+(pCVar6,(wchar_t *)local_3bc);
    local_8._0_1_ = 0x1a;
    uVar7 = DuiLib::CDuiString::operator+(pCVar6,local_338);
    local_8._0_1_ = 0x1b;
    goto LAB_00408786;
  case 0x40:
    pwVar9 = L"media_player_text";
    break;
  case 0x41:
    pwVar9 = L"play_pause_text";
    break;
  case 0x42:
    pwVar9 = L"media_stop_text";
    break;
  case 0x43:
    pwVar9 = L"pre_track_text";
    break;
  case 0x44:
    pwVar9 = L"next_track_text";
    break;
  case 0x45:
    pwVar9 = L"volume_up_text";
    break;
  case 0x46:
    pwVar9 = L"volume_down_text";
    break;
  case 0x47:
    pwVar9 = L"mute_text";
    break;
  case 0x48:
    pwVar9 = L"browser_home_text";
    break;
  case 0x49:
    pwVar9 = L"browser_favorites_text";
    break;
  case 0x4a:
    pwVar9 = L"browser_forward_text";
    break;
  case 0x4b:
    pwVar9 = L"browser_backward_text";
    break;
  case 0x4c:
    pwVar9 = L"browser_stop_text";
    break;
  case 0x4d:
    pwVar9 = L"browser_refresh_text";
    break;
  case 0x4e:
    pwVar9 = L"browser_search_text";
    break;
  case 0x4f:
    pwVar9 = L"email_text";
    break;
  case 0x50:
    pwVar9 = L"calculator_text";
    break;
  case 0x51:
    pwVar9 = L"my_computer_text";
    break;
  case 0x68:
    pwVar9 = L"report_up_text";
    break;
  case 0x69:
    pwVar9 = L"report_down_text";
    break;
  case 0x70:
    pwVar9 = L"report_cycle_text";
    break;
  case 0x71:
    pwVar9 = L"juji_text";
    break;
  case 0x79:
    DuiLib::CDuiString::CDuiString(local_1a0);
    local_8._0_1_ = 0x1c;
    DuiLib::CDuiString::CDuiString(local_224);
    local_8._0_1_ = 0x1d;
    DuiLib::CDuiString::CDuiString(local_11c);
    pCVar6 = local_338;
    local_8._0_1_ = 0x1e;
    pwVar9 = L"set_gun_text";
    pCVar5 = DuiLib::CResourceManager::GetInstance();
    pCVar6 = (CDuiString *)DuiLib::CResourceManager::GetText(pCVar5,(wchar_t *)pCVar6,pwVar9);
    pcVar8 = operator=_exref;
    local_8._0_1_ = 0x1f;
    DuiLib::CDuiString::operator=(local_1a0,pCVar6);
    local_8._0_1_ = 0x1e;
    DuiLib::CDuiString::~CDuiString(local_338);
    DuiLib::CDuiString::operator=(local_224,local_22c);
    DuiLib::CDuiString::operator=(local_11c,local_22c + 0x32);
    (**(code **)(*(int *)*local_230 + 0x34))(0);
    pCVar6 = (CDuiString *)DuiLib::CDuiString::operator+(local_1a0,local_2b4);
    local_8._0_1_ = 0x20;
    pCVar6 = (CDuiString *)DuiLib::CDuiString::operator+(pCVar6,(wchar_t *)local_3bc);
    local_8._0_1_ = 0x21;
    uVar7 = DuiLib::CDuiString::operator+(pCVar6,local_338);
    local_8._0_1_ = 0x22;
LAB_00408786:
    (*pcVar8)(uVar7);
    DuiLib::CDuiString::~CDuiString(local_338);
    DuiLib::CDuiString::~CDuiString(local_3bc);
    DuiLib::CDuiString::~CDuiString(local_2b4);
    DuiLib::CDuiString::~CDuiString(local_11c);
    DuiLib::CDuiString::~CDuiString(local_224);
    local_8 = (uint)local_8._1_3_ << 8;
    DuiLib::CDuiString::~CDuiString(local_1a0);
    goto LAB_00408a16;
  }
  DuiLib::CDuiString::operator=(local_98,pwVar9);
LAB_00408a16:
  iVar3 = *(int *)*local_230;
  pwVar9 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
  (**(code **)(iVar3 + 0x2c))(pwVar9);
  DuiLib::CDuiString::~CDuiString(local_98);
  ExceptionList = local_10;
  return;
}


