// Program: SM809 mouse Software.exe
// Function: FUN_0040ac10
// Entry: 0040ac10
// Body: 0040ac10 - 0040ae8a
// Signature: undefined FUN_0040ac10(void * this, int param_1)


void __thiscall FUN_0040ac10(void *this,int param_1)

{
  int *piVar1;
  int *piVar2;
  CDuiString *pCVar3;
  wchar_t *pwVar4;
  int iVar5;
  int iVar6;
  undefined4 *puVar7;
  undefined4 *puVar8;
  undefined4 in_stack_fffffec8;
  undefined4 uVar9;
  CDuiString local_118 [132];
  CDuiString local_94 [132];
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00421d99;
  local_10 = ExceptionList;
  piVar1 = *(int **)(param_1 + 0x108);
  if (piVar1 == *(int **)((int)this + 0x1c0)) {
    if (*(int *)((int)this + 0x1c) != 0) {
      ExceptionList = &local_10;
      FUN_0040ba50((int)this);
      ExceptionList = local_10;
      return;
    }
  }
  else {
    iVar6 = 0;
    piVar2 = (int *)((int)this + 0x3a8);
    while (piVar1 != (int *)piVar2[0x5a]) {
      if (piVar1 == (int *)*piVar2) {
        ExceptionList = &local_10;
        pCVar3 = (CDuiString *)(**(code **)(*(int *)*piVar2 + 0x28))(local_94);
        local_8 = 1;
        pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(pCVar3);
        uVar9 = 0x40ad5b;
        iVar5 = _wtoi(pwVar4);
        local_8 = 0xffffffff;
        DuiLib::CDuiString::~CDuiString(local_94);
        if (iVar5 < -0x7f) {
          iVar5 = -0x7f;
          pwVar4 = L"-127";
LAB_0040ad93:
          uVar9 = 0x40ad9f;
          (**(code **)(**(int **)((int)this + iVar6 * 4 + 0x3a8) + 0x2c))(pwVar4);
        }
        else if (0x7f < iVar5) {
          iVar5 = 0x7f;
          pwVar4 = L"127";
          goto LAB_0040ad93;
        }
        *(int *)((int)this + iVar6 * 0xc + 0x2c) = iVar5;
        goto LAB_0040ae17;
      }
      if (piVar1 == (int *)piVar2[-0x5a]) {
        ExceptionList = &local_10;
        pCVar3 = (CDuiString *)(**(code **)(*(int *)piVar2[-0x5a] + 0x28))(local_118);
        local_8 = 2;
        pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(pCVar3);
        uVar9 = 0x40ace3;
        iVar5 = _wtoi(pwVar4);
        local_8 = 0xffffffff;
        DuiLib::CDuiString::~CDuiString(local_118);
        if (iVar5 < 10) {
          iVar5 = 10;
          pwVar4 = L"10";
LAB_0040ad1e:
          uVar9 = 0x40ad2a;
          (**(code **)(**(int **)((int)this + iVar6 * 4 + 0x240) + 0x2c))(pwVar4);
        }
        else if (0x4f6 < iVar5) {
          iVar5 = 0x4f6;
          pwVar4 = L"1270";
          goto LAB_0040ad1e;
        }
        *(short *)((int)this + iVar6 * 0xc + 0x32) = (short)iVar5;
        goto LAB_0040ae17;
      }
      iVar6 = iVar6 + 1;
      piVar2 = piVar2 + 1;
      if (0x1d < iVar6) {
        return;
      }
    }
    ExceptionList = &local_10;
    pCVar3 = (CDuiString *)
             (**(code **)(*(int *)piVar2[0x5a] + 0x28))
                       (local_94,DAT_00432008 ^ (uint)(local_94 + 0x90));
    local_8 = 0;
    pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(pCVar3);
    uVar9 = 0x40adcc;
    iVar5 = _wtoi(pwVar4);
    local_8 = 0xffffffff;
    DuiLib::CDuiString::~CDuiString(local_94);
    if (iVar5 < -0x7f) {
      iVar5 = -0x7f;
      pwVar4 = L"-127";
LAB_0040ae04:
      uVar9 = 0x40ae10;
      (**(code **)(**(int **)((int)this + iVar6 * 4 + 0x510) + 0x2c))(pwVar4);
    }
    else if (0x7f < iVar5) {
      iVar5 = 0x7f;
      pwVar4 = L"127";
      goto LAB_0040ae04;
    }
    *(int *)((int)this + iVar6 * 0xc + 0x28) = iVar5;
LAB_0040ae17:
    iVar6 = *(int *)((int)this + 0x1c);
    if ((iVar6 != 0) && (*(int *)(iVar6 + 0xcc) == 0)) {
      *(undefined1 *)(iVar6 + 200) = *(undefined1 *)((int)this + 0x20);
      puVar7 = (undefined4 *)((int)this + 0x28);
      puVar8 = (undefined4 *)(*(int *)((int)this + 0x1c) + 0xd8);
      for (iVar6 = 0x5a; iVar6 != 0; iVar6 = iVar6 + -1) {
        *puVar8 = *puVar7;
        puVar7 = puVar7 + 1;
        puVar8 = puVar8 + 1;
      }
      FUN_00403350();
      iVar6 = FUN_00404200(*(uint *)((int)this + 0x1ac),DAT_00432aa8,in_stack_fffffec8,uVar9,0);
      if (iVar6 != 0) {
        SendMessageW(*(HWND *)((int)this + 0x14),0x467,0,0);
      }
    }
  }
  ExceptionList = local_10;
  return;
}


