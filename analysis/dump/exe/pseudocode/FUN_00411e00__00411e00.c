// Program: SM809 mouse Software.exe
// Function: FUN_00411e00
// Entry: 00411e00
// Body: 00411e00 - 00412515
// Signature: undefined FUN_00411e00(void * this, int param_1, int param_2)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_00411e00(void *this,int param_1,int param_2)

{
  CContainerUI *pCVar1;
  uint uVar2;
  CDuiString *pCVar3;
  wchar_t *pwVar4;
  undefined4 uVar5;
  CDuiString *this_00;
  CDuiString *this_01;
  CControlUI *pCVar6;
  code *pcVar7;
  int iVar8;
  code *pcVar9;
  CDuiString local_244 [132];
  undefined4 local_1c0;
  int local_1bc;
  CControlUI *local_1b8;
  CContainerUI *local_1b4;
  CContainerUI *local_1b0;
  char local_1a9;
  CControlUI *local_1a8;
  CControlUI *local_1a4;
  CDuiString local_1a0 [132];
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00422b01;
  local_10 = ExceptionList;
  uVar2 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  local_1bc = param_2;
  local_1a8 = this;
  local_14 = uVar2;
  DuiLib::CDuiString::CDuiString(local_1a0);
  local_8 = 0;
  DuiLib::CDuiString::CDuiString(local_98);
  local_8._0_1_ = 1;
  local_1b0 = (CContainerUI *)
              (*(code *)**(undefined4 **)(*(int *)((int)this + 0x360) + 0x558))(param_1,uVar2);
  local_1b4 = (CContainerUI *)
              (*(code *)**(undefined4 **)(*(int *)((int)this + 0x360) + 0x558))(local_1bc);
  DuiLib::CDuiString::CDuiString(local_11c);
  local_8._0_1_ = 2;
  local_1a9 = *(char *)((int)local_1a8 + param_1 * 0x10 + 0x26);
  pCVar6 = (CControlUI *)(uint)*(byte *)((int)this + param_1 * 0x10 + 0x25);
  local_1b8 = *(CControlUI **)((int)local_1a8 + param_1 * 0x10 + 0x2c);
  local_1c0 = *(undefined4 *)((int)local_1a8 + (param_1 + 3) * 0x10);
  local_1a4 = pCVar6;
  DuiLib::CDuiString::Format
            ((CDuiString *)(param_1 * 2),(wchar_t *)local_11c,&DAT_00424f54,
             (uint)*(ushort *)((int)local_1a8 + param_1 * 0x10 + 0x28));
  pCVar3 = FUN_00402370(local_244,pCVar6);
  local_8._0_1_ = 3;
  DuiLib::CDuiString::operator=(local_98,pCVar3);
  local_8 = CONCAT31(local_8._1_3_,2);
  DuiLib::CDuiString::~CDuiString(local_244);
  pCVar1 = local_1b0;
  pcVar9 = operator_wchar_t_const__exref;
  if (local_1a9 == '\x01') {
    if (local_1a4 + -0xf0 < (CControlUI *)0x5) {
      local_1a4 = DuiLib::CContainerUI::FindSubControl(local_1b0,L"key");
      if (local_1a4 != (CControlUI *)0x0) {
        iVar8 = *(int *)local_1a4;
        pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
        (**(code **)(iVar8 + 0x2c))(pwVar4);
        pwVar4 = L"res=\'skins/mouse.png\' dest=\'10,4,32,36\'";
LAB_00411fa9:
        DuiLib::CControlUI::SetBkImage(local_1a4,pwVar4);
      }
    }
    else {
      local_1a4 = DuiLib::CContainerUI::FindSubControl(local_1b0,L"key");
      if (local_1a4 != (CControlUI *)0x0) {
        iVar8 = *(int *)local_1a4;
        pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
        (**(code **)(iVar8 + 0x2c))(pwVar4);
        pwVar4 = L"res=\'skins/keyboard_key_action.png\' dest=\'5,6,35,24\'";
        goto LAB_00411fa9;
      }
    }
    pCVar6 = DuiLib::CContainerUI::FindSubControl(local_1b0,L"action");
    (**(code **)(*(int *)pCVar6 + 0x34))(1);
    (**(code **)(*(int *)pCVar6 + 0x2c))(L"key_down_action");
    pcVar7 = SetBkImage_exref;
    DuiLib::CControlUI::SetBkImage(pCVar6,L"res=\'skins/macro_key_down.png\' dest=\'5,6,21,24\'");
    local_1a4 = DuiLib::CContainerUI::FindSubControl(local_1b0,L"delay");
    if (local_1a4 != (CControlUI *)0x0) {
      iVar8 = *(int *)local_1a4;
      pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_11c);
LAB_004121c1:
      (**(code **)(iVar8 + 0x2c))(pwVar4);
      pcVar7 = SetBkImage_exref;
    }
  }
  else if (local_1a9 == '\x02') {
    if (local_1a4 + -0xf0 < (CControlUI *)0x5) {
      local_1a4 = DuiLib::CContainerUI::FindSubControl(local_1b0,L"key");
      if (local_1a4 != (CControlUI *)0x0) {
        iVar8 = *(int *)local_1a4;
        pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
        (**(code **)(iVar8 + 0x2c))(pwVar4);
        pwVar4 = L"res=\'skins/mouse.png\' dest=\'10,4,32,36\'";
LAB_00412088:
        DuiLib::CControlUI::SetBkImage(local_1a4,pwVar4);
      }
    }
    else {
      local_1a4 = DuiLib::CContainerUI::FindSubControl(local_1b0,L"key");
      if (local_1a4 != (CControlUI *)0x0) {
        iVar8 = *(int *)local_1a4;
        pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
        (**(code **)(iVar8 + 0x2c))(pwVar4);
        pwVar4 = L"res=\'skins/keyboard_key_action.png\' dest=\'5,6,35,24\'";
        goto LAB_00412088;
      }
    }
    pCVar6 = DuiLib::CContainerUI::FindSubControl(local_1b0,L"action");
    (**(code **)(*(int *)pCVar6 + 0x34))(1);
    (**(code **)(*(int *)pCVar6 + 0x2c))(L"key_up_action");
    pcVar7 = SetBkImage_exref;
    DuiLib::CControlUI::SetBkImage(pCVar6,L"res=\'skins/macro_key_up.png\' dest=\'5,6,21,24\'");
    local_1a4 = DuiLib::CContainerUI::FindSubControl(local_1b0,L"delay");
    if (local_1a4 != (CControlUI *)0x0) {
      iVar8 = *(int *)local_1a4;
      pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_11c);
      goto LAB_004121c1;
    }
  }
  else {
    pcVar7 = SetBkImage_exref;
    if (local_1a9 == '\0') {
      local_1a4 = DuiLib::CContainerUI::FindSubControl(local_1b0,L"key");
      if (local_1a4 != (CControlUI *)0x0) {
        (**(code **)(*(int *)local_1a4 + 0x2c))(L"mouse_move_text");
        DuiLib::CControlUI::SetBkImage(local_1a4,L"res=\'skins/move.png\' dest=\'2,2,28,28\'");
      }
      pCVar6 = DuiLib::CContainerUI::FindSubControl(pCVar1,L"action");
      (**(code **)(*(int *)pCVar6 + 0x34))(1);
      (**(code **)(*(int *)pCVar6 + 0x34))(0);
      DuiLib::CDuiString::Format(this_00,(wchar_t *)local_98,L"X: %d Y: %d",local_1b8,local_1c0);
      iVar8 = *(int *)pCVar6;
      pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
      (**(code **)(iVar8 + 0x2c))(pwVar4);
      pcVar7 = SetBkImage_exref;
      DuiLib::CControlUI::SetBkImage(pCVar6,L"");
      local_1b8 = DuiLib::CContainerUI::FindSubControl(local_1b0,L"delay");
      pcVar9 = operator_wchar_t_const__exref;
      if (local_1b8 != (CControlUI *)0x0) {
        iVar8 = *(int *)local_1b8;
        pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_11c);
        goto LAB_004121c1;
      }
    }
  }
  local_1b0 = (CContainerUI *)(uint)*(byte *)((int)local_1a8 + local_1bc * 0x10 + 0x25);
  local_1a9 = *(char *)((int)local_1a8 + local_1bc * 0x10 + 0x26);
  local_1c0 = *(undefined4 *)((int)local_1a8 + (local_1bc + 3) * 0x10);
  pCVar3 = (CDuiString *)0x0;
  if (local_1bc != *(int *)((int)local_1a8 + 0x2a4) + -1) {
    pCVar3 = (CDuiString *)(uint)*(ushort *)((int)local_1a8 + local_1bc * 0x10 + 0x28);
  }
  local_1a8 = *(CControlUI **)((int)local_1a8 + local_1bc * 0x10 + 0x2c);
  DuiLib::CDuiString::Format(pCVar3,(wchar_t *)local_11c,&DAT_00424f54,pCVar3);
  pCVar3 = FUN_00402370(local_244,local_1b0);
  local_8._0_1_ = 4;
  DuiLib::CDuiString::operator=(local_98,pCVar3);
  local_8 = CONCAT31(local_8._1_3_,2);
  DuiLib::CDuiString::~CDuiString(local_244);
  pCVar1 = local_1b4;
  if (local_1a9 == '\x01') {
    if ((int)local_1b0 - 0xf0U < 5) {
      local_1a8 = DuiLib::CContainerUI::FindSubControl(local_1b4,L"key");
      if (local_1a8 != (CControlUI *)0x0) {
        iVar8 = *(int *)local_1a8;
        uVar5 = (*pcVar9)();
        (**(code **)(iVar8 + 0x2c))(uVar5);
        pwVar4 = L"res=\'skins/mouse.png\' dest=\'10,4,32,36\'";
LAB_004122df:
        DuiLib::CControlUI::SetBkImage(local_1a8,pwVar4);
      }
    }
    else {
      local_1a8 = DuiLib::CContainerUI::FindSubControl(local_1b4,L"key");
      if (local_1a8 != (CControlUI *)0x0) {
        iVar8 = *(int *)local_1a8;
        uVar5 = (*pcVar9)();
        (**(code **)(iVar8 + 0x2c))(uVar5);
        pwVar4 = L"res=\'skins/keyboard_key_action.png\' dest=\'5,6,35,24\'";
        goto LAB_004122df;
      }
    }
    pCVar6 = DuiLib::CContainerUI::FindSubControl(local_1b4,L"action");
    (**(code **)(*(int *)pCVar6 + 0x34))(1);
    (**(code **)(*(int *)pCVar6 + 0x2c))(L"key_down_action");
    DuiLib::CControlUI::SetBkImage(pCVar6,L"res=\'skins/macro_key_down.png\' dest=\'5,6,21,24\'");
    pCVar6 = DuiLib::CContainerUI::FindSubControl(local_1b4,L"delay");
    if (pCVar6 == (CControlUI *)0x0) goto LAB_004124da;
    iVar8 = *(int *)pCVar6;
    pwVar4 = (wchar_t *)(*pcVar9)();
  }
  else if (local_1a9 == '\x02') {
    if ((int)local_1b0 - 0xf0U < 5) {
      local_1a8 = DuiLib::CContainerUI::FindSubControl(local_1b4,L"key");
      if (local_1a8 != (CControlUI *)0x0) {
        iVar8 = *(int *)local_1a8;
        uVar5 = (*pcVar9)();
        (**(code **)(iVar8 + 0x2c))(uVar5);
        pwVar4 = L"res=\'skins/mouse.png\' dest=\'10,4,32,36\'";
LAB_004123b4:
        DuiLib::CControlUI::SetBkImage(local_1a8,pwVar4);
      }
    }
    else {
      local_1a8 = DuiLib::CContainerUI::FindSubControl(local_1b4,L"key");
      if (local_1a8 != (CControlUI *)0x0) {
        iVar8 = *(int *)local_1a8;
        uVar5 = (*pcVar9)();
        (**(code **)(iVar8 + 0x2c))(uVar5);
        pwVar4 = L"res=\'skins/keyboard_key_action.png\' dest=\'5,6,35,24\'";
        goto LAB_004123b4;
      }
    }
    pCVar6 = DuiLib::CContainerUI::FindSubControl(local_1b4,L"action");
    (**(code **)(*(int *)pCVar6 + 0x34))(1);
    (**(code **)(*(int *)pCVar6 + 0x2c))(L"key_up_action");
    DuiLib::CControlUI::SetBkImage(pCVar6,L"res=\'skins/macro_key_up.png\' dest=\'5,6,21,24\'");
    pCVar6 = DuiLib::CContainerUI::FindSubControl(local_1b4,L"delay");
    if (pCVar6 == (CControlUI *)0x0) goto LAB_004124da;
    iVar8 = *(int *)pCVar6;
    pwVar4 = (wchar_t *)(*pcVar9)();
  }
  else {
    if (local_1a9 != '\0') goto LAB_004124da;
    local_1b8 = DuiLib::CContainerUI::FindSubControl(local_1b4,L"key");
    if (local_1b8 != (CControlUI *)0x0) {
      (**(code **)(*(int *)local_1b8 + 0x2c))(L"mouse_move_text");
      (*pcVar7)(L"res=\'skins/move.png\' dest=\'2,2,28,28\'");
    }
    pCVar6 = DuiLib::CContainerUI::FindSubControl(pCVar1,L"action");
    (**(code **)(*(int *)pCVar6 + 0x34))(1);
    (**(code **)(*(int *)pCVar6 + 0x34))(0);
    DuiLib::CDuiString::Format(this_01,(wchar_t *)local_98,L"X: %d Y: %d",local_1a8,local_1c0);
    iVar8 = *(int *)pCVar6;
    pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    (**(code **)(iVar8 + 0x2c))(pwVar4);
    DuiLib::CControlUI::SetBkImage(pCVar6,L"");
    pCVar6 = DuiLib::CContainerUI::FindSubControl(local_1b4,L"delay");
    if (pCVar6 == (CControlUI *)0x0) goto LAB_004124da;
    iVar8 = *(int *)pCVar6;
    pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_11c);
  }
  (**(code **)(iVar8 + 0x2c))(pwVar4);
LAB_004124da:
  DuiLib::CDuiString::~CDuiString(local_11c);
  DuiLib::CDuiString::~CDuiString(local_98);
  DuiLib::CDuiString::~CDuiString(local_1a0);
  ExceptionList = local_10;
  return;
}


