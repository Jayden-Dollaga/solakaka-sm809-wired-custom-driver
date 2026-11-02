// Program: SM809 mouse Software.exe
// Function: FUN_0040a3d0
// Entry: 0040a3d0
// Body: 0040a3d0 - 0040a99c
// Signature: undefined FUN_0040a3d0(void * this, int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_0040a3d0(void *this,int param_1)

{
  int iVar1;
  uint uVar2;
  int *piVar3;
  CMenuWnd *pCVar4;
  undefined4 uVar5;
  wchar_t *pwVar6;
  int iVar7;
  CDuiString *this_00;
  undefined4 *puVar8;
  undefined4 *puVar9;
  int local_140;
  CDuiString *local_13c;
  undefined4 *local_138;
  CDuiString local_134 [132];
  CDuiString local_b0 [132];
  tagRECT local_2c;
  int local_1c;
  void *local_18;
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00421cd7;
  local_10 = ExceptionList;
  uVar2 = DAT_00432008 ^ (uint)(local_b0 + 0xac);
  ExceptionList = &local_10;
  iVar7 = *(int *)(param_1 + 0x108);
  local_18 = this;
  local_14 = uVar2;
  if (iVar7 == *(int *)((int)this + 0x1b4)) {
    FUN_0040b080((int)this);
  }
  else if (iVar7 == *(int *)((int)this + 0x1b8)) {
    FUN_0040b3b0(this);
  }
  else if (iVar7 == *(int *)((int)this + 0x678)) {
    FUN_0040c9c0((int)this);
  }
  else if (iVar7 == *(int *)((int)this + 0x67c)) {
    FUN_0040cda0(this);
  }
  else if (iVar7 == *(int *)((int)this + 0x1bc)) {
    pCVar4 = *(CMenuWnd **)((int)this + 0x18);
    if (pCVar4 != (CMenuWnd *)0x0) {
      DuiLib::CMenuWnd::~CMenuWnd(pCVar4);
      FUN_0041feb7(pCVar4);
      *(undefined4 *)((int)this + 0x18) = 0;
    }
    GetWindowRect(*(HWND *)((int)this + 0x14),&local_2c);
    piVar3 = (int *)(**(code **)(**(int **)((int)this + 0x1bc) + 0x50))();
    iVar7 = *piVar3;
    iVar1 = piVar3[3];
    pCVar4 = operator_new(0x770);
    local_8 = 0;
    uVar5 = DuiLib::CMenuWnd::CMenuWnd(pCVar4);
    local_8 = 0xffffffff;
    *(undefined4 *)((int)this + 0x18) = uVar5;
    DuiLib::CDuiPoint::CDuiPoint((CDuiPoint *)&local_1c);
    local_1c = iVar7 + local_2c.left;
    local_18 = (void *)(local_2c.top + iVar1);
    DuiLib::CMenuWnd::Init
              (*(CMenuWnd **)((int)this + 0x18),0,L"gunmenu.xml",local_1c,local_18,
               *(undefined4 *)((int)this + 0x10),0,6);
  }
  else if (iVar7 == *(int *)((int)this + 0x680)) {
    pCVar4 = *(CMenuWnd **)((int)this + 0x18);
    if (pCVar4 != (CMenuWnd *)0x0) {
      DuiLib::CMenuWnd::~CMenuWnd(pCVar4);
      FUN_0041feb7(pCVar4);
      *(undefined4 *)((int)this + 0x18) = 0;
    }
    GetWindowRect(*(HWND *)((int)this + 0x14),&local_2c);
    piVar3 = (int *)(**(code **)(**(int **)((int)this + 0x680) + 0x50))();
    iVar7 = *piVar3;
    iVar1 = piVar3[3];
    pCVar4 = operator_new(0x770);
    local_8 = 1;
    uVar5 = DuiLib::CMenuWnd::CMenuWnd(pCVar4);
    local_8 = 0xffffffff;
    *(undefined4 *)((int)this + 0x18) = uVar5;
    DuiLib::CDuiPoint::CDuiPoint((CDuiPoint *)&local_1c);
    local_1c = iVar7 + local_2c.left;
    local_18 = (void *)(local_2c.top + iVar1);
    DuiLib::CMenuWnd::Init
              (*(CMenuWnd **)((int)this + 0x18),0,L"gundirmenu.xml",local_1c,local_18,
               *(undefined4 *)((int)this + 0x10),0,6);
  }
  else {
    local_13c = (CDuiString *)((int)this + 0x28);
    local_140 = 0x1e;
    local_138 = (undefined4 *)((int)this + 0x3a8);
    do {
      iVar7 = *(int *)(param_1 + 0x108);
      if (iVar7 == local_138[0x1e]) {
        (**(code **)(*(int *)*local_138 + 0x28))(local_b0);
        local_8 = 2;
        pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_b0);
        iVar7 = _wtoi(pwVar6);
        iVar7 = iVar7 + 1;
LAB_0040a658:
        *(int *)(local_13c + 4) = iVar7;
        DuiLib::CDuiString::Format(local_13c,(wchar_t *)local_b0,&DAT_00424f54,iVar7);
        iVar7 = *(int *)*local_138;
        pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_b0);
LAB_0040a68f:
        uVar5 = 0x40a693;
        (**(code **)(iVar7 + 0x2c))();
        iVar7 = *(int *)((int)this + 0x1c);
        if ((iVar7 != 0) && (*(int *)(iVar7 + 0xcc) == 0)) {
          *(undefined1 *)(iVar7 + 200) = *(undefined1 *)((int)this + 0x20);
          puVar8 = (undefined4 *)((int)this + 0x28);
          puVar9 = (undefined4 *)(*(int *)((int)this + 0x1c) + 0xd8);
          for (iVar7 = 0x5a; iVar7 != 0; iVar7 = iVar7 + -1) {
            *puVar9 = *puVar8;
            puVar8 = puVar8 + 1;
            puVar9 = puVar9 + 1;
          }
          FUN_00403350();
          this = local_18;
          iVar7 = FUN_00404200(*(uint *)((int)local_18 + 0x1ac),DAT_00432aa8,uVar5,pwVar6,0);
          if (iVar7 != 0) {
            SendMessageW(*(HWND *)((int)this + 0x14),0x467,0,0);
          }
        }
        this_00 = local_b0;
LAB_0040a94d:
        local_8 = 0xffffffff;
        DuiLib::CDuiString::~CDuiString(this_00);
      }
      else {
        if (iVar7 == local_138[0x3c]) {
          (**(code **)(*(int *)*local_138 + 0x28))(local_b0);
          local_8 = 3;
          pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_b0);
          iVar7 = _wtoi(pwVar6);
          iVar7 = iVar7 + -1;
          goto LAB_0040a658;
        }
        if (iVar7 == local_138[0x78]) {
          (**(code **)(*(int *)local_138[0x5a] + 0x28))(local_b0);
          local_8 = 4;
          pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_b0);
          iVar7 = _wtoi(pwVar6);
          iVar7 = iVar7 + 1;
LAB_0040a76c:
          *(int *)local_13c = iVar7;
          DuiLib::CDuiString::Format(local_13c,(wchar_t *)local_b0,&DAT_00424f54,iVar7);
          iVar7 = *(int *)local_138[0x5a];
          pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_b0);
          goto LAB_0040a68f;
        }
        if (iVar7 == local_138[0x96]) {
          (**(code **)(*(int *)local_138[0x5a] + 0x28))(local_b0);
          local_8 = 5;
          pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_b0);
          iVar7 = _wtoi(pwVar6);
          iVar7 = iVar7 + -1;
          goto LAB_0040a76c;
        }
        if (iVar7 == local_138[-0x3c]) {
          (**(code **)(*(int *)local_138[-0x5a] + 0x28))(local_b0);
          local_8 = 6;
          pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_b0);
          iVar7 = _wtoi(pwVar6);
          *(short *)(local_13c + 10) = (short)(iVar7 + 1);
          DuiLib::CDuiString::Format(local_13c,(wchar_t *)local_b0,&DAT_00424f54,iVar7 + 1);
          iVar7 = *(int *)local_138[-0x5a];
          pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_b0);
          goto LAB_0040a68f;
        }
        if (iVar7 == local_138[-0x1e]) {
          (**(code **)(*(int *)local_138[-0x5a] + 0x28))(local_134,uVar2);
          local_8 = 7;
          pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_134);
          iVar7 = _wtoi(pwVar6);
          iVar7 = iVar7 + -1;
          if (iVar7 < 1) {
            iVar7 = 1;
          }
          *(short *)(local_13c + 10) = (short)iVar7;
          DuiLib::CDuiString::Format(local_13c,(wchar_t *)local_134,&DAT_00424f54,iVar7);
          iVar7 = *(int *)local_138[-0x5a];
          pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_134);
          uVar5 = 0x40a8e4;
          (**(code **)(iVar7 + 0x2c))();
          iVar7 = *(int *)((int)this + 0x1c);
          if ((iVar7 != 0) && (*(int *)(iVar7 + 0xcc) == 0)) {
            *(undefined1 *)(iVar7 + 200) = *(undefined1 *)((int)this + 0x20);
            puVar8 = (undefined4 *)((int)this + 0x28);
            puVar9 = (undefined4 *)(*(int *)((int)this + 0x1c) + 0xd8);
            for (iVar7 = 0x5a; iVar7 != 0; iVar7 = iVar7 + -1) {
              *puVar9 = *puVar8;
              puVar8 = puVar8 + 1;
              puVar9 = puVar9 + 1;
            }
            FUN_00403350();
            this = local_18;
            iVar7 = FUN_00404200(*(uint *)((int)local_18 + 0x1ac),DAT_00432aa8,uVar5,pwVar6,0);
            if (iVar7 != 0) {
              SendMessageW(*(HWND *)((int)this + 0x14),0x467,0,0);
            }
          }
          this_00 = local_134;
          goto LAB_0040a94d;
        }
      }
      local_13c = local_13c + 0xc;
      local_138 = local_138 + 1;
      local_140 = local_140 + -1;
    } while (local_140 != 0);
  }
  ExceptionList = local_10;
  return;
}


