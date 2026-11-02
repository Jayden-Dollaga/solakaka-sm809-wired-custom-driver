// Program: SM809 mouse Software.exe
// Function: FUN_0040f1e0
// Entry: 0040f1e0
// Body: 0040f1e0 - 0040f6da
// Signature: undefined FUN_0040f1e0(void * this, int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_0040f1e0(void *this,int param_1)

{
  undefined4 *puVar1;
  CMenuWnd *pCVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  int iVar6;
  undefined4 *puVar7;
  CDuiString *pCVar8;
  wchar_t *pwVar9;
  undefined4 uVar10;
  int iVar11;
  int *piVar12;
  int extraout_ECX;
  int iVar13;
  undefined4 uVar14;
  undefined4 uVar15;
  undefined4 uVar16;
  CDuiString local_e4 [132];
  int local_60;
  int iStack_5c;
  int iStack_58;
  int iStack_54;
  CMenuWnd *local_50;
  tagRECT local_4c;
  tagRECT local_3c;
  int local_2c;
  int local_28;
  undefined4 local_24;
  undefined4 uStack_20;
  int iStack_1c;
  int iStack_18;
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_004226e1;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_e4 + 0xe0);
  iVar6 = *(int *)(param_1 + 0x108);
  if (iVar6 == *(int *)((int)this + 0x33c)) {
    ExceptionList = &local_10;
    FUN_00410390((int)this);
  }
  else if (iVar6 == *(int *)((int)this + 0x340)) {
    ExceptionList = &local_10;
    FUN_00410690(this);
  }
  else if (iVar6 == *(int *)((int)this + 0x38c)) {
    ExceptionList = &local_10;
    FUN_004131f0((int)this);
  }
  else if (iVar6 == *(int *)((int)this + 0x390)) {
    ExceptionList = &local_10;
    FUN_004135c0(this);
  }
  else {
    if (iVar6 == *(int *)((int)this + 0x364)) {
      ExceptionList = &local_10;
      iVar6 = (**(code **)(*(int *)(*(int *)((int)this + 0x360) + 0x6c8) + 8))();
      if (iVar6 < 1) {
        ExceptionList = local_10;
        return;
      }
      iVar13 = iVar6 + -1;
      puVar7 = (undefined4 *)((int)this + iVar6 * 0x10 + 0x24);
      uVar3 = puVar7[1];
      uVar4 = puVar7[2];
      uVar5 = puVar7[3];
      puVar1 = (undefined4 *)((int)this + iVar6 * 0x10 + 0x14);
      uVar10 = *puVar1;
      uVar14 = puVar1[1];
      uVar15 = puVar1[2];
      uVar16 = puVar1[3];
      puVar1 = (undefined4 *)((int)this + iVar6 * 0x10 + 0x14);
      *puVar1 = *puVar7;
      puVar1[1] = uVar3;
      puVar1[2] = uVar4;
      puVar1[3] = uVar5;
    }
    else {
      if (iVar6 != *(int *)((int)this + 0x368)) {
        if (iVar6 != *(int *)((int)this + 0x36c)) {
          if (iVar6 == *(int *)((int)this + 0x370)) {
            if (*(int *)((int)this + 0x1c) == 0) {
              return;
            }
            ExceptionList = &local_10;
            memset((void *)((int)this + 0x24),0,0x280);
            *(undefined4 *)((int)this + 0x2a4) = 0;
            *(undefined4 *)((int)this + 0x2c0) = 0;
            *(undefined4 *)((int)this + 0x2b4) = 0xffffffff;
            *(undefined4 *)((int)this + 700) = 0xffffffff;
            FUN_004116c0((int)this);
            FUN_00411220((int)this);
            FUN_00411740(this,-1);
            ExceptionList = local_10;
            return;
          }
          if (iVar6 != *(int *)((int)this + 0x39c)) {
            if (iVar6 == *(int *)((int)this + 0x344)) {
              pCVar2 = *(CMenuWnd **)((int)this + 0x18);
              ExceptionList = &local_10;
              if (pCVar2 != (CMenuWnd *)0x0) {
                DuiLib::CMenuWnd::~CMenuWnd(pCVar2);
                FUN_0041feb7(pCVar2);
                *(undefined4 *)((int)this + 0x18) = 0;
              }
              GetWindowRect(*(HWND *)((int)this + 0x14),&local_3c);
              piVar12 = (int *)(**(code **)(**(int **)((int)this + 0x344) + 0x50))();
              local_60 = *piVar12;
              iStack_5c = piVar12[1];
              iStack_58 = piVar12[2];
              iStack_54 = piVar12[3];
              local_50 = operator_new(0x770);
              local_8 = 2;
              uVar10 = DuiLib::CMenuWnd::CMenuWnd(local_50);
              local_8 = 0xffffffff;
              *(undefined4 *)((int)this + 0x18) = uVar10;
              DuiLib::CDuiPoint::CDuiPoint((CDuiPoint *)&local_2c);
              iVar13 = local_60 + local_3c.left;
              uVar10 = *(undefined4 *)((int)this + 0x10);
              iVar6 = local_3c.top + iStack_54;
              pwVar9 = L"macromenu.xml";
              local_2c = iVar13;
              local_28 = iVar6;
            }
            else {
              if (iVar6 != *(int *)((int)this + 0x394)) {
                return;
              }
              pCVar2 = *(CMenuWnd **)((int)this + 0x18);
              ExceptionList = &local_10;
              if (pCVar2 != (CMenuWnd *)0x0) {
                DuiLib::CMenuWnd::~CMenuWnd(pCVar2);
                FUN_0041feb7(pCVar2);
                *(undefined4 *)((int)this + 0x18) = 0;
              }
              GetWindowRect(*(HWND *)((int)this + 0x14),&local_4c);
              piVar12 = (int *)(**(code **)(**(int **)((int)this + 0x394) + 0x50))();
              local_60 = *piVar12;
              iStack_5c = piVar12[1];
              iStack_58 = piVar12[2];
              iStack_54 = piVar12[3];
              local_50 = operator_new(0x770);
              local_8 = 3;
              uVar10 = DuiLib::CMenuWnd::CMenuWnd(local_50);
              local_8 = 0xffffffff;
              *(undefined4 *)((int)this + 0x18) = uVar10;
              DuiLib::CDuiPoint::CDuiPoint((CDuiPoint *)&iStack_1c);
              iVar13 = local_60 + local_4c.left;
              uVar10 = *(undefined4 *)((int)this + 0x10);
              iVar6 = local_4c.top + iStack_54;
              pwVar9 = L"macrodirmenu.xml";
              iStack_1c = iVar13;
              iStack_18 = iVar6;
            }
            DuiLib::CMenuWnd::Init
                      (*(CMenuWnd **)((int)this + 0x18),0,pwVar9,iVar13,iVar6,uVar10,0,6);
            ExceptionList = local_10;
            return;
          }
          if (*(int *)((int)this + 0x1c) == 0) {
            return;
          }
          if (*(int *)(*(int *)((int)this + 0x1c) + 0xd0) == 1) {
            return;
          }
          if (0x23 < *(int *)((int)this + 0x2a4)) {
            return;
          }
          ExceptionList = &local_10;
          pCVar8 = (CDuiString *)
                   (**(code **)(**(int **)((int)this + 0x3ac) + 0x28))(local_e4,local_14);
          local_8 = 0;
          pwVar9 = DuiLib::CDuiString::operator_wchar_t_const_(pCVar8);
          local_28 = _wtoi(pwVar9);
          local_8 = 0xffffffff;
          DuiLib::CDuiString::~CDuiString(local_e4);
          pCVar8 = (CDuiString *)(**(code **)(**(int **)((int)this + 0x3b0) + 0x28))(local_e4);
          local_8 = 1;
          pwVar9 = DuiLib::CDuiString::operator_wchar_t_const_(pCVar8);
          local_50 = (CMenuWnd *)_wtoi(pwVar9);
          local_8 = 0xffffffff;
          DuiLib::CDuiString::~CDuiString(local_e4);
          uStack_20 = CONCAT22(uStack_20._2_2_,10);
          iStack_1c = local_28;
          iStack_18 = (int)local_50;
          local_24._0_3_ = CONCAT21(0xf6,(undefined1)local_24);
          if (-1 < *(int *)((int)this + 700)) {
            iVar6 = *(int *)((int)this + 700) + 1;
            *(undefined4 *)((int)this + 0x2c0) = 1;
            *(int *)((int)this + 0x2b4) = iVar6;
            *(int *)((int)this + 0x2b0) = iVar6;
          }
          FUN_004111b0(this,local_24,uStack_20,local_28,local_50);
          FUN_004116c0(extraout_ECX);
          FUN_00411220((int)this);
          *(undefined4 *)((int)this + 0x2c0) = 0;
          ExceptionList = local_10;
          return;
        }
        iVar6 = *(int *)((int)this + 700);
        if (iVar6 < 0) {
          return;
        }
        iVar13 = *(int *)((int)this + 0x2a4);
        ExceptionList = &local_10;
        if (iVar6 < iVar13) {
          puVar7 = (undefined4 *)(iVar6 * 0x10 + 0x24 + (int)this);
          iVar11 = iVar6;
          do {
            iVar11 = iVar11 + 1;
            *puVar7 = puVar7[4];
            puVar7[1] = puVar7[5];
            puVar7[2] = puVar7[6];
            puVar7[3] = puVar7[7];
            iVar13 = *(int *)((int)this + 0x2a4);
            puVar7 = puVar7 + 4;
          } while (iVar11 < iVar13);
        }
        *(int *)((int)this + 0x2a4) = iVar13 + -1;
        (**(code **)(*(int *)(*(int *)((int)this + 0x360) + 0x558) + 0x1c))(iVar6);
        iVar13 = *(int *)((int)this + 0x2a4);
        if (iVar13 < 1) {
          *(undefined4 *)((int)this + 700) = 0xffffffff;
        }
        piVar12 = (int *)(*(int *)((int)this + 0x360) + 0x6c8);
        if (iVar6 < iVar13) {
          (**(code **)(*piVar12 + 0xc))(iVar6,0);
          FUN_004116c0((int)this);
          ExceptionList = local_10;
          return;
        }
        (**(code **)(*piVar12 + 0xc))(iVar13 + -1);
        FUN_004116c0((int)this);
        ExceptionList = local_10;
        return;
      }
      ExceptionList = &local_10;
      iVar6 = (**(code **)(*(int *)(*(int *)((int)this + 0x360) + 0x6c8) + 8))();
      if (iVar6 < 0) {
        ExceptionList = local_10;
        return;
      }
      if (*(int *)((int)this + 0x2a4) + -1 <= iVar6) {
        ExceptionList = local_10;
        return;
      }
      iVar13 = iVar6 + 1;
      puVar7 = (undefined4 *)((int)this + iVar6 * 0x10 + 0x24);
      uVar3 = puVar7[1];
      uVar4 = puVar7[2];
      uVar5 = puVar7[3];
      puVar1 = (undefined4 *)((int)this + iVar6 * 0x10 + 0x34);
      uVar10 = *puVar1;
      uVar14 = puVar1[1];
      uVar15 = puVar1[2];
      uVar16 = puVar1[3];
      puVar1 = (undefined4 *)((int)this + iVar6 * 0x10 + 0x34);
      *puVar1 = *puVar7;
      puVar1[1] = uVar3;
      puVar1[2] = uVar4;
      puVar1[3] = uVar5;
    }
    puVar7 = (undefined4 *)((int)this + iVar6 * 0x10 + 0x24);
    *puVar7 = uVar10;
    puVar7[1] = uVar14;
    puVar7[2] = uVar15;
    puVar7[3] = uVar16;
    FUN_00411e00(this,iVar6,iVar13);
    (**(code **)(*(int *)(*(int *)((int)this + 0x360) + 0x6c8) + 0xc))(iVar13,0);
    FUN_004116c0((int)this);
  }
  ExceptionList = local_10;
  return;
}


