// Program: SM809 mouse Software.exe
// Function: FUN_00411220
// Entry: 00411220
// Body: 00411220 - 004116b6
// Signature: undefined FUN_00411220(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_00411220(int param_1)

{
  int iVar1;
  int iVar2;
  CControlUI *this;
  CDuiString *pCVar3;
  wchar_t *pwVar4;
  undefined4 uVar5;
  int iVar6;
  CDuiString *this_00;
  code *pcVar7;
  CDuiString local_38c [132];
  CDuiString *local_308;
  int local_304;
  int local_300;
  char *local_2fc;
  CControlUI *local_2f8;
  char local_2f1;
  CControlUI *local_2f0;
  CDialogBuilder local_2ec [332];
  CDuiString local_1a0 [132];
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00422991;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  local_300 = param_1;
  (**(code **)(*(int *)(*(int *)(param_1 + 0x360) + 0x558) + 0x20))(local_14);
  DuiLib::CDuiString::CDuiString(local_98);
  local_8 = 0;
  DuiLib::CDuiString::CDuiString(local_1a0);
  local_8._0_1_ = 1;
  DuiLib::CDuiString::CDuiString(local_11c);
  local_8._0_1_ = 2;
  DuiLib::CDialogBuilder::CDialogBuilder(local_2ec);
  local_8._0_1_ = 3;
  local_304 = 0;
  iVar6 = *(int *)(local_300 + 0x2a4);
  if (0 < iVar6) {
    local_2fc = (char *)(local_300 + 0x26);
    pcVar7 = operator_wchar_t_const__exref;
    do {
      this = DuiLib::CDialogBuilder::Create
                       (local_2ec,L"macrolistitem.xml",0,0,*(undefined4 *)(local_300 + 0x10),0);
      local_2f0 = (CControlUI *)(uint)(byte)local_2fc[-1];
      local_2f8 = *(CControlUI **)(local_2fc + 6);
      local_2f1 = *local_2fc;
      local_308 = *(CDuiString **)(local_2fc + 10);
      DuiLib::CDuiString::Format
                (local_308,(wchar_t *)local_11c,&DAT_00424f54,(uint)*(ushort *)(local_2fc + 2));
      pCVar3 = FUN_00402370(local_38c,local_2f0);
      local_8._0_1_ = 4;
      DuiLib::CDuiString::operator=(local_98,pCVar3);
      local_8._0_1_ = 3;
      DuiLib::CDuiString::~CDuiString(local_38c);
      (**(code **)(*(int *)this + 0x88))(0x1e);
      (**(code **)(*(int *)(*(int *)(local_300 + 0x360) + 0x558) + 0x10))(this);
      if (local_2f1 == '\x01') {
        if (local_2f0 + -0xf0 < (CControlUI *)0x5) {
          local_2f0 = DuiLib::CContainerUI::FindSubControl((CContainerUI *)this,L"key");
          if (local_2f0 != (CControlUI *)0x0) {
            iVar6 = *(int *)local_2f0;
            pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
            (**(code **)(iVar6 + 0x2c))(pwVar4);
            pwVar4 = L"res=\'skins/mouse.png\' dest=\'2,2,28,28\'";
LAB_00411417:
            DuiLib::CControlUI::SetBkImage(local_2f0,pwVar4);
            pcVar7 = operator_wchar_t_const__exref;
          }
        }
        else {
          local_2f0 = DuiLib::CContainerUI::FindSubControl((CContainerUI *)this,L"key");
          if (local_2f0 != (CControlUI *)0x0) {
            iVar6 = *(int *)local_2f0;
            pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
            (**(code **)(iVar6 + 0x2c))(pwVar4);
            pwVar4 = L"res=\'skins/keyboard_key_action.png\' dest=\'5,6,35,24\'";
            goto LAB_00411417;
          }
        }
        local_2f0 = DuiLib::CContainerUI::FindSubControl((CContainerUI *)this,L"action");
        if (local_2f0 != (CControlUI *)0x0) {
          (**(code **)(*(int *)local_2f0 + 0x2c))(L"key_down_action");
          pwVar4 = L"res=\'skins/macro_key_down.png\' dest=\'5,6,21,24\'";
LAB_0041144d:
          DuiLib::CControlUI::SetBkImage(local_2f0,pwVar4);
        }
LAB_00411459:
        local_2f0 = DuiLib::CContainerUI::FindSubControl((CContainerUI *)this,L"delay");
        if (local_2f0 != (CControlUI *)0x0) {
          iVar6 = *(int *)local_2f0;
          uVar5 = (*pcVar7)();
LAB_004115f9:
          (**(code **)(iVar6 + 0x2c))(uVar5);
        }
      }
      else {
        if (local_2f1 == '\x02') {
          if (local_2f0 + -0xf0 < (CControlUI *)0x5) {
            local_2f0 = DuiLib::CContainerUI::FindSubControl((CContainerUI *)this,L"key");
            if (local_2f0 != (CControlUI *)0x0) {
              iVar6 = *(int *)local_2f0;
              pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
              (**(code **)(iVar6 + 0x2c))(pwVar4);
              pwVar4 = L"res=\'skins/mouse.png\' dest=\'2,2,28,28\'";
LAB_004114fc:
              DuiLib::CControlUI::SetBkImage(local_2f0,pwVar4);
              pcVar7 = operator_wchar_t_const__exref;
            }
          }
          else {
            local_2f0 = DuiLib::CContainerUI::FindSubControl((CContainerUI *)this,L"key");
            if (local_2f0 != (CControlUI *)0x0) {
              iVar6 = *(int *)local_2f0;
              pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
              (**(code **)(iVar6 + 0x2c))(pwVar4);
              pwVar4 = L"res=\'skins/keyboard_key_action.png\' dest=\'5,6,35,24\'";
              goto LAB_004114fc;
            }
          }
          local_2f0 = DuiLib::CContainerUI::FindSubControl((CContainerUI *)this,L"action");
          if (local_2f0 != (CControlUI *)0x0) {
            (**(code **)(*(int *)local_2f0 + 0x2c))(L"key_up_action");
            pwVar4 = L"res=\'skins/macro_key_up.png\' dest=\'5,6,21,24\'";
            goto LAB_0041144d;
          }
          goto LAB_00411459;
        }
        if (local_2f1 == '\0') {
          local_2f0 = DuiLib::CContainerUI::FindSubControl((CContainerUI *)this,L"key");
          if (local_2f0 != (CControlUI *)0x0) {
            (**(code **)(*(int *)local_2f0 + 0x2c))(L"mouse_move_text");
            DuiLib::CControlUI::SetBkImage(local_2f0,L"res=\'skins/move.png\' dest=\'2,2,28,28\'");
          }
          local_2f0 = DuiLib::CContainerUI::FindSubControl((CContainerUI *)this,L"action");
          if (local_2f0 != (CControlUI *)0x0) {
            (**(code **)(*(int *)local_2f0 + 0x34))(0);
            DuiLib::CDuiString::Format
                      (this_00,(wchar_t *)local_98,L"X: %d Y: %d",local_2f8,local_308);
            iVar6 = *(int *)local_2f0;
            pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
            (**(code **)(iVar6 + 0x2c))(pwVar4);
            pcVar7 = operator_wchar_t_const__exref;
          }
          local_2f8 = DuiLib::CContainerUI::FindSubControl((CContainerUI *)this,L"delay");
          if (local_2f8 == (CControlUI *)0x0) goto LAB_004115fd;
          iVar6 = *(int *)local_2f8;
          uVar5 = (*pcVar7)();
          goto LAB_004115f9;
        }
      }
LAB_004115fd:
      local_2fc = local_2fc + 0x10;
      local_304 = local_304 + 1;
      iVar6 = *(int *)(local_300 + 0x2a4);
    } while (local_304 < iVar6);
  }
  iVar2 = local_300;
  iVar1 = *(int *)(*(int *)(local_300 + 0x360) + 0x6c8);
  if (*(int *)(local_300 + 0x2c0) == 0) {
    (**(code **)(iVar1 + 0xc))(iVar6 + -1,0);
    (**(code **)(**(int **)(iVar2 + 0x360) + 0x1d0))();
  }
  else {
    (**(code **)(iVar1 + 0xc))(*(int *)(local_300 + 0x2b4) + -1);
    DuiLib::CPaintManagerUI::SetTimer
              (*(CPaintManagerUI **)(iVar2 + 0x10),*(CControlUI **)(iVar2 + 0x360),3,0x32);
  }
  DuiLib::CDialogBuilder::~CDialogBuilder(local_2ec);
  DuiLib::CDuiString::~CDuiString(local_11c);
  DuiLib::CDuiString::~CDuiString(local_1a0);
  DuiLib::CDuiString::~CDuiString(local_98);
  ExceptionList = local_10;
  return;
}


