// Program: SM809 mouse Software.exe
// Function: FUN_0040e5e0
// Entry: 0040e5e0
// Body: 0040e5e0 - 0040e9b5
// Signature: undefined FUN_0040e5e0(void * this, int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_0040e5e0(void *this,int param_1)

{
  int iVar1;
  uint uVar2;
  CDuiString *pCVar3;
  wchar_t *pwVar4;
  uint uVar5;
  CDuiString *this_00;
  CDuiString *this_01;
  CDuiString *this_02;
  uint uVar6;
  undefined4 uVar7;
  CDuiString local_1a8 [132];
  uint local_124;
  uint local_120;
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_004224fd;
  local_10 = ExceptionList;
  uVar2 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  iVar1 = *(int *)(param_1 + 0x108);
  local_14 = uVar2;
  if (iVar1 == *(int *)((int)this + 100)) {
    ExceptionList = &local_10;
    DuiLib::CDuiString::CDuiString(local_98);
    local_8 = 0;
    local_124 = *(uint *)(DAT_00432aa0 + 0x104);
    pCVar3 = (CDuiString *)(**(code **)(**(int **)((int)this + 100) + 0x28))(local_11c);
    local_8._0_1_ = 1;
    DuiLib::CDuiString::operator=(local_98,pCVar3);
    local_8 = (uint)local_8._1_3_ << 8;
    DuiLib::CDuiString::~CDuiString(local_11c);
    pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    local_120 = _wtoi(pwVar4);
    if ((int)local_120 < 0x100) {
      if ((int)local_120 < 0) {
        local_120 = 0;
        uVar7 = 0;
        goto LAB_0040e6bc;
      }
    }
    else {
      local_120 = 0xff;
      uVar7 = 0xff;
LAB_0040e6bc:
      DuiLib::CDuiString::Format(this_00,(wchar_t *)local_98,&DAT_00424f54,uVar7);
      iVar1 = **(int **)((int)this + 100);
      pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
      (**(code **)(iVar1 + 0x2c))(pwVar4);
    }
    uVar2 = local_124 >> 0x10 & 0xff;
    uVar5 = (local_124 & 0xffff) >> 8;
    uVar6 = (uVar2 << 8 | uVar5) << 8 | local_120 & 0xff;
    uVar5 = (uVar6 | 0xffffff00) << 0x10 | uVar5 << 8;
  }
  else {
    if (iVar1 != *(int *)((int)this + 0x68)) {
      if (iVar1 != *(int *)((int)this + 0x6c)) {
        return;
      }
      ExceptionList = &local_10;
      DuiLib::CDuiString::CDuiString(local_11c);
      local_8 = 4;
      local_124 = *(uint *)(DAT_00432aa0 + 0x104);
      pCVar3 = (CDuiString *)(**(code **)(**(int **)((int)this + 0x6c) + 0x28))(local_1a8,uVar2);
      local_8._0_1_ = 5;
      DuiLib::CDuiString::operator=(local_11c,pCVar3);
      local_8 = CONCAT31(local_8._1_3_,4);
      DuiLib::CDuiString::~CDuiString(local_1a8);
      pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_11c);
      uVar2 = _wtoi(pwVar4);
      if ((int)uVar2 < 0x100) {
        if ((int)uVar2 < 0) {
          DuiLib::CDuiString::Format(this_02,(wchar_t *)local_11c,&DAT_00424f54,0);
          iVar1 = **(int **)((int)this + 0x6c);
          pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_11c);
          (**(code **)(iVar1 + 0x2c))(pwVar4);
          uVar2 = 0;
        }
      }
      else {
        DuiLib::CDuiString::Format(this_02,(wchar_t *)local_11c,&DAT_00424f54,0xff);
        iVar1 = **(int **)((int)this + 0x6c);
        pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_11c);
        (**(code **)(iVar1 + 0x2c))(pwVar4);
        uVar2 = 0xff;
      }
      uVar5 = (local_124 & 0xffff) >> 8;
      uVar6 = (uVar5 | (uVar2 & 0xff) << 8) << 8 | local_124 & 0xff;
      uVar2 = (uVar6 | 0xffffff00) << 0x10 | uVar2 & 0xff | uVar5 << 8;
      DuiLib::CColorPaletteUI::SetSelectColor(*(CColorPaletteUI **)((int)this + 0x60),uVar2);
      DuiLib::CControlUI::SetBkColor(*(CControlUI **)((int)this + 0x5c),uVar2);
      pCVar3 = local_11c;
      goto LAB_0040e987;
    }
    ExceptionList = &local_10;
    DuiLib::CDuiString::CDuiString(local_98);
    local_8 = 2;
    local_124 = *(uint *)(DAT_00432aa0 + 0x104);
    pCVar3 = (CDuiString *)(**(code **)(**(int **)((int)this + 0x68) + 0x28))(local_11c);
    local_8._0_1_ = 3;
    DuiLib::CDuiString::operator=(local_98,pCVar3);
    local_8 = CONCAT31(local_8._1_3_,2);
    DuiLib::CDuiString::~CDuiString(local_11c);
    pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    local_120 = _wtoi(pwVar4);
    if ((int)local_120 < 0x100) {
      if ((int)local_120 < 0) {
        local_120 = 0;
        uVar7 = 0;
        goto LAB_0040e7e9;
      }
    }
    else {
      local_120 = 0xff;
      uVar7 = 0xff;
LAB_0040e7e9:
      DuiLib::CDuiString::Format(this_01,(wchar_t *)local_98,&DAT_00424f54,uVar7);
      iVar1 = **(int **)((int)this + 0x68);
      pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
      (**(code **)(iVar1 + 0x2c))(pwVar4);
    }
    uVar5 = local_124 >> 0x10 & 0xff;
    uVar6 = (uVar5 << 8 | local_120 & 0xff) << 8 | local_124 & 0xff;
    uVar5 = (uVar6 | 0xffffff00) << 0x10 | uVar5;
    uVar2 = (local_120 & 0xff) << 8;
  }
  DuiLib::CColorPaletteUI::SetSelectColor(*(CColorPaletteUI **)((int)this + 0x60),uVar5 | uVar2);
  DuiLib::CControlUI::SetBkColor(*(CControlUI **)((int)this + 0x5c),uVar5 | uVar2);
  pCVar3 = local_98;
LAB_0040e987:
  *(uint *)(DAT_00432aa0 + 0x104) = uVar6;
  DuiLib::CDuiString::~CDuiString(pCVar3);
  ExceptionList = local_10;
  return;
}


