// Program: SM809 mouse Software.exe
// Function: FUN_0040fb70
// Entry: 0040fb70
// Body: 0040fb70 - 00410010
// Signature: undefined FUN_0040fb70(void * this, int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_0040fb70(void *this,int param_1)

{
  int iVar1;
  CDuiString *pCVar2;
  wchar_t *pwVar3;
  int iVar4;
  CControlUI *pCVar5;
  CContainerUI *pCVar6;
  CDuiString *this_00;
  CDuiString *this_01;
  CDuiString *this_02;
  CDuiString *this_03;
  CDuiString *this_04;
  undefined4 uVar7;
  CDuiString local_1a4 [132];
  CContainerUI *local_120;
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_004227d5;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  iVar4 = *(int *)(param_1 + 0x108);
  if (iVar4 == *(int *)((int)this + 0x374)) {
    ExceptionList = &local_10;
    (**(code **)((int)this + 0x328))(local_14);
    ExceptionList = local_10;
    return;
  }
  if (iVar4 == *(int *)((int)this + 0x378)) {
    if (*(int *)((int)this + 700) < 0) {
      return;
    }
    ExceptionList = &local_10;
    DuiLib::CDuiString::CDuiString(local_98);
    local_8 = 0;
    pCVar2 = (CDuiString *)(**(code **)(**(int **)((int)this + 0x378) + 0x28))(local_11c);
    local_8._0_1_ = 1;
    pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(pCVar2);
    iVar4 = _wtoi(pwVar3);
    local_8 = (uint)local_8._1_3_ << 8;
    DuiLib::CDuiString::~CDuiString(local_11c);
    if (iVar4 < 10) {
      iVar4 = 10;
      uVar7 = 10;
LAB_0040fc45:
      DuiLib::CDuiString::Format(this_00,(wchar_t *)local_98,&DAT_00424f54,uVar7);
      iVar1 = **(int **)((int)this + 0x378);
      pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
      (**(code **)(iVar1 + 0x2c))(pwVar3);
    }
    else if (0xffff < iVar4) {
      iVar4 = 0xffff;
      uVar7 = 0xffff;
      goto LAB_0040fc45;
    }
    *(short *)((int)this + *(int *)((int)this + 700) * 0x10 + 0x28) = (short)iVar4;
    local_120 = (CContainerUI *)
                (*(code *)**(undefined4 **)(*(int *)((int)this + 0x360) + 0x558))
                          (*(undefined4 *)((int)this + 700));
    if (local_120 != (CContainerUI *)0x0) {
      DuiLib::CDuiString::Format(this_01,(wchar_t *)local_98,&DAT_00424f54,iVar4);
      pwVar3 = L"delay";
      pCVar6 = local_120;
LAB_0040fcc5:
      pCVar5 = DuiLib::CContainerUI::FindSubControl(pCVar6,pwVar3);
      if (pCVar5 != (CControlUI *)0x0) {
        iVar4 = *(int *)pCVar5;
        pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
        (**(code **)(iVar4 + 0x2c))(pwVar3);
      }
    }
LAB_0040fce5:
    FUN_004116c0((int)this);
  }
  else {
    if (iVar4 == *(int *)((int)this + 0x348)) {
      if (*(int *)((int)this + 0x1c) == 0) {
        return;
      }
      ExceptionList = &local_10;
      FUN_00411bc0((int)this);
      ExceptionList = local_10;
      return;
    }
    if (iVar4 == *(int *)((int)this + 0x388)) {
      ExceptionList = &local_10;
      DuiLib::CDuiString::CDuiString(local_98);
      local_8 = 2;
      pCVar2 = (CDuiString *)(**(code **)(**(int **)((int)this + 0x388) + 0x28))(local_11c);
      local_8._0_1_ = 3;
      pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(pCVar2);
      iVar4 = _wtoi(pwVar3);
      local_8 = CONCAT31(local_8._1_3_,2);
      DuiLib::CDuiString::~CDuiString(local_11c);
      if (iVar4 < 1) {
        iVar4 = 1;
        uVar7 = 1;
LAB_0040fd87:
        DuiLib::CDuiString::Format(this_02,(wchar_t *)local_98,&DAT_00424f54,uVar7);
        iVar1 = **(int **)((int)this + 0x388);
        pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
        (**(code **)(iVar1 + 0x2c))(pwVar3);
      }
      else if (0xff < iVar4) {
        iVar4 = 0xff;
        uVar7 = 0xff;
        goto LAB_0040fd87;
      }
      *(int *)((int)this + 0x2f4) = iVar4;
      FUN_004116c0((int)this);
      pCVar2 = local_98;
      goto LAB_0040ffed;
    }
    if (iVar4 != *(int *)((int)this + 0x3a4)) {
      if (iVar4 != *(int *)((int)this + 0x3a8)) {
        return;
      }
      ExceptionList = &local_10;
      DuiLib::CDuiString::CDuiString(local_11c);
      local_8 = 6;
      if (-1 < *(int *)((int)this + 700)) {
        pCVar2 = (CDuiString *)(**(code **)(**(int **)((int)this + 0x3a8) + 0x28))(local_1a4);
        local_8._0_1_ = 7;
        pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(pCVar2);
        iVar4 = _wtoi(pwVar3);
        local_8 = CONCAT31(local_8._1_3_,6);
        DuiLib::CDuiString::~CDuiString(local_1a4);
        if (iVar4 < -0x7fff) {
          iVar4 = -0x7fff;
          pwVar3 = L"-32767";
LAB_0040ff59:
          (**(code **)(**(int **)((int)this + 0x3a8) + 0x2c))(pwVar3);
        }
        else if (0x7fff < iVar4) {
          iVar4 = 0x7fff;
          pwVar3 = L"32767";
          goto LAB_0040ff59;
        }
        *(int *)((int)this + (*(int *)((int)this + 700) + 3) * 0x10) = iVar4;
        local_120 = *(CContainerUI **)((int)this + *(int *)((int)this + 700) * 0x10 + 0x2c);
        pCVar6 = (CContainerUI *)
                 (*(code *)**(undefined4 **)(*(int *)((int)this + 0x360) + 0x558))
                           (*(int *)((int)this + 700));
        if (pCVar6 != (CContainerUI *)0x0) {
          DuiLib::CDuiString::Format(this_04,(wchar_t *)local_11c,L"X: %d Y: %d",local_120,iVar4);
          pCVar5 = DuiLib::CContainerUI::FindSubControl(pCVar6,L"action");
          if (pCVar5 != (CControlUI *)0x0) {
            iVar4 = *(int *)pCVar5;
            pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_11c);
            (**(code **)(iVar4 + 0x2c))(pwVar3);
          }
        }
        FUN_004116c0((int)this);
      }
      pCVar2 = local_11c;
      goto LAB_0040ffed;
    }
    ExceptionList = &local_10;
    DuiLib::CDuiString::CDuiString(local_98);
    local_8 = 4;
    if (-1 < *(int *)((int)this + 700)) {
      pCVar2 = (CDuiString *)(**(code **)(**(int **)((int)this + 0x3a4) + 0x28))(local_11c);
      local_8._0_1_ = 5;
      pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(pCVar2);
      iVar4 = _wtoi(pwVar3);
      local_8 = CONCAT31(local_8._1_3_,4);
      DuiLib::CDuiString::~CDuiString(local_11c);
      if (iVar4 < -0x7fff) {
        iVar4 = -0x7fff;
        pwVar3 = L"-32767";
LAB_0040fe5f:
        (**(code **)(**(int **)((int)this + 0x3a4) + 0x2c))(pwVar3);
      }
      else if (0x7fff < iVar4) {
        iVar4 = 0x7fff;
        pwVar3 = L"32767";
        goto LAB_0040fe5f;
      }
      *(int *)((int)this + *(int *)((int)this + 700) * 0x10 + 0x2c) = iVar4;
      local_120 = *(CContainerUI **)((int)this + (*(int *)((int)this + 700) + 3) * 0x10);
      pCVar6 = (CContainerUI *)
               (*(code *)**(undefined4 **)(*(int *)((int)this + 0x360) + 0x558))
                         (*(int *)((int)this + 700));
      if (pCVar6 != (CContainerUI *)0x0) {
        DuiLib::CDuiString::Format(this_03,(wchar_t *)local_98,L"X: %d Y: %d",iVar4,local_120);
        pwVar3 = L"action";
        goto LAB_0040fcc5;
      }
      goto LAB_0040fce5;
    }
  }
  pCVar2 = local_98;
LAB_0040ffed:
  DuiLib::CDuiString::~CDuiString(pCVar2);
  ExceptionList = local_10;
  return;
}


