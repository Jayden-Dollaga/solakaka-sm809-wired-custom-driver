// Program: SM809 mouse Software.exe
// Function: FUN_0041d950
// Entry: 0041d950
// Body: 0041d950 - 0041dd3c
// Signature: undefined FUN_0041d950(void * this, int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_0041d950(void *this,int param_1)

{
  int iVar1;
  uint uVar2;
  CDuiString *pCVar3;
  wchar_t *pwVar4;
  CDuiString *this_00;
  CDuiString *this_01;
  uint uVar5;
  undefined4 uVar6;
  CDuiString local_1a4 [132];
  CDuiString *local_120;
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_004239bd;
  local_10 = ExceptionList;
  uVar2 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  iVar1 = *(int *)(param_1 + 0x108);
  local_14 = uVar2;
  if (iVar1 == *(int *)((int)this + 0x774)) {
    ExceptionList = &local_10;
    DuiLib::CDuiString::CDuiString(local_98);
    local_8 = 0;
    uVar2 = *(ushort *)((int)this + 0x788) & 0xff;
    uVar5 = (uint)(*(ushort *)((int)this + 0x788) >> 8);
    pCVar3 = (CDuiString *)(**(code **)(**(int **)((int)this + 0x774) + 0x28))(local_11c);
    local_8._0_1_ = 1;
    DuiLib::CDuiString::operator=(local_98,pCVar3);
    local_8 = (uint)local_8._1_3_ << 8;
    DuiLib::CDuiString::~CDuiString(local_11c);
    pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar3 = (CDuiString *)_wtoi(pwVar4);
    if ((int)pCVar3 < 0x100) {
      local_120 = pCVar3;
      if ((int)pCVar3 < 0) {
        local_120 = (CDuiString *)0x0;
        uVar6 = 0;
        goto LAB_0041da42;
      }
    }
    else {
      local_120 = (CDuiString *)0xff;
      uVar6 = 0xff;
LAB_0041da42:
      DuiLib::CDuiString::Format(pCVar3,(wchar_t *)local_98,&DAT_00424f54,uVar6);
      iVar1 = **(int **)((int)this + 0x774);
      pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
      (**(code **)(iVar1 + 0x2c))(pwVar4);
    }
    uVar5 = (uVar5 << 8 | (uint)local_120 & 0xff | 0xffffff00) << 0x10 | uVar5 << 8;
  }
  else {
    if (iVar1 != *(int *)((int)this + 0x778)) {
      if (iVar1 != *(int *)((int)this + 0x77c)) {
        return;
      }
      ExceptionList = &local_10;
      DuiLib::CDuiString::CDuiString(local_11c);
      local_8 = 4;
      local_120 = (CDuiString *)
                  (((uint)(*(ushort *)((int)this + 0x788) >> 8) |
                   (*(ushort *)((int)this + 0x788) & 0xff) << 8) << 8 |
                  (uint)*(byte *)((int)this + 0x78a));
      pCVar3 = (CDuiString *)(**(code **)(**(int **)((int)this + 0x77c) + 0x28))(local_1a4,uVar2);
      local_8._0_1_ = 5;
      DuiLib::CDuiString::operator=(local_11c,pCVar3);
      local_8 = CONCAT31(local_8._1_3_,4);
      DuiLib::CDuiString::~CDuiString(local_1a4);
      pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_11c);
      uVar2 = _wtoi(pwVar4);
      if ((int)uVar2 < 0x100) {
        if ((int)uVar2 < 0) {
          uVar2 = 0;
          uVar6 = 0;
          goto LAB_0041dc89;
        }
      }
      else {
        uVar2 = 0xff;
        uVar6 = 0xff;
LAB_0041dc89:
        DuiLib::CDuiString::Format(this_01,(wchar_t *)local_11c,&DAT_00424f54,uVar6);
        iVar1 = **(int **)((int)this + 0x77c);
        pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_11c);
        (**(code **)(iVar1 + 0x2c))(pwVar4);
      }
      uVar5 = ((uint)local_120 & 0xffff) >> 8;
      uVar5 = (uVar5 << 8 | (uint)local_120 & 0xff | 0xffffff00) << 0x10 | uVar2 & 0xff | uVar5 << 8
      ;
      DuiLib::CColorPaletteUI::SetSelectColor(*(CColorPaletteUI **)((int)this + 0x780),uVar5);
      DuiLib::CControlUI::SetBkColor(*(CControlUI **)((int)this + 0x770),uVar5);
      pCVar3 = local_11c;
      goto LAB_0041dd13;
    }
    ExceptionList = &local_10;
    DuiLib::CDuiString::CDuiString(local_98);
    local_8 = 2;
    local_120 = (CDuiString *)
                (((uint)(*(ushort *)((int)this + 0x788) >> 8) |
                 (*(ushort *)((int)this + 0x788) & 0xff) << 8) << 8 |
                (uint)*(byte *)((int)this + 0x78a));
    pCVar3 = (CDuiString *)(**(code **)(**(int **)((int)this + 0x778) + 0x28))(local_11c);
    local_8._0_1_ = 3;
    DuiLib::CDuiString::operator=(local_98,pCVar3);
    local_8 = CONCAT31(local_8._1_3_,2);
    DuiLib::CDuiString::~CDuiString(local_11c);
    pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    uVar2 = _wtoi(pwVar4);
    if ((int)uVar2 < 0x100) {
      if ((int)uVar2 < 0) {
        uVar2 = 0;
        uVar6 = 0;
        goto LAB_0041db77;
      }
    }
    else {
      uVar2 = 0xff;
      uVar6 = 0xff;
LAB_0041db77:
      DuiLib::CDuiString::Format(this_00,(wchar_t *)local_98,&DAT_00424f54,uVar6);
      iVar1 = **(int **)((int)this + 0x778);
      pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
      (**(code **)(iVar1 + 0x2c))(pwVar4);
    }
    uVar2 = (uVar2 & 0xff) << 8;
    uVar5 = (uVar2 | (uint)local_120 & 0xff | 0xffffff00) << 0x10 | (uint)local_120 >> 0x10;
  }
  uVar5 = uVar5 | uVar2;
  DuiLib::CColorPaletteUI::SetSelectColor(*(CColorPaletteUI **)((int)this + 0x780),uVar5);
  DuiLib::CControlUI::SetBkColor(*(CControlUI **)((int)this + 0x770),uVar5);
  pCVar3 = local_98;
LAB_0041dd13:
  *(uint *)((int)this + 0x788) = uVar5;
  DuiLib::CDuiString::~CDuiString(pCVar3);
  ExceptionList = local_10;
  return;
}


