// Program: SM809 mouse Software.exe
// Function: FUN_00406a40
// Entry: 00406a40
// Body: 00406a40 - 00406c02
// Signature: undefined FUN_00406a40(void * this, int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_00406a40(void *this,int param_1)

{
  int iVar1;
  char cVar2;
  uint uVar3;
  int *piVar4;
  CMenuWnd *pCVar5;
  undefined4 uVar6;
  CMenuUI *pCVar7;
  int iVar8;
  int iVar9;
  int iVar10;
  int local_34;
  int *local_30;
  tagRECT local_2c;
  int local_1c;
  int local_18;
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00421727;
  local_10 = ExceptionList;
  uVar3 = DAT_00432008 ^ (int)register0x00000010 - 4U;
  ExceptionList = &local_10;
  local_30 = (int *)((int)this + 0x20);
  local_34 = 0;
  local_14 = uVar3;
  do {
    if (*(int *)(param_1 + 0x108) == *local_30) {
      pCVar5 = *(CMenuWnd **)((int)this + 0x1c);
      *(int *)((int)this + 0x18) = local_34;
      if (pCVar5 != (CMenuWnd *)0x0) {
        DuiLib::CMenuWnd::~CMenuWnd(pCVar5);
        FUN_0041feb7(pCVar5);
        *(undefined4 *)((int)this + 0x1c) = 0;
      }
      GetWindowRect(*(HWND *)((int)this + 0x14),&local_2c);
      piVar4 = (int *)(**(code **)(*(int *)*local_30 + 0x50))(uVar3);
      iVar8 = *piVar4;
      iVar1 = piVar4[1];
      iVar9 = piVar4[3];
      pCVar5 = operator_new(0x770);
      local_8 = 0;
      uVar6 = DuiLib::CMenuWnd::CMenuWnd(pCVar5);
      local_8 = 0xffffffff;
      *(undefined4 *)((int)this + 0x1c) = uVar6;
      DuiLib::CDuiPoint::CDuiPoint((CDuiPoint *)&local_1c);
      local_1c = iVar8 + local_2c.left;
      local_18 = local_2c.top + iVar9;
      DuiLib::CMenuWnd::Init
                (*(CMenuWnd **)((int)this + 0x1c),0,L"buttonmenu.xml",local_1c,local_18,
                 *(undefined4 *)((int)this + 0x10),0,6);
      pCVar7 = DuiLib::CMenuWnd::GetMenuUI(*(CMenuWnd **)((int)this + 0x1c));
      iVar8 = (**(code **)(*(int *)(pCVar7 + 0x558) + 0xc))();
      iVar10 = 0;
      iVar9 = 0;
      if (0 < iVar8) {
        do {
          piVar4 = (int *)(*(code *)**(undefined4 **)(pCVar7 + 0x558))(iVar9);
          cVar2 = (**(code **)(*piVar4 + 0xf4))();
          if (cVar2 != '\0') {
            iVar10 = iVar10 + 1;
          }
          iVar9 = iVar9 + 1;
        } while (iVar9 < iVar8);
      }
      iVar8 = GetSystemMetrics(1);
      if (iVar8 <= local_18 + iVar10 * 0x19) {
        local_18 = local_2c.top + -4 + iVar1 + iVar10 * -0x19;
        iVar8 = *(int *)((int)this + 0x1c);
        *(int *)(iVar8 + 0x24) = local_1c;
        *(int *)(iVar8 + 0x28) = local_18;
        DuiLib::CMenuWnd::ResizeMenu(*(CMenuWnd **)((int)this + 0x1c));
      }
    }
    local_34 = local_34 + 1;
    local_30 = local_30 + 1;
  } while (local_34 < 0x40);
  ExceptionList = local_10;
  return;
}


