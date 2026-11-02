// Program: SM809 mouse Software.exe
// Function: FUN_0040b650
// Entry: 0040b650
// Body: 0040b650 - 0040b9d9
// Signature: undefined FUN_0040b650(void * this, uint param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_0040b650(void *this,uint param_1)

{
  undefined4 uVar1;
  uint uVar2;
  wchar_t *pwVar3;
  CDuiString *this_00;
  CDuiString *this_01;
  CDuiString *this_02;
  int iVar4;
  undefined4 *puVar5;
  int local_a0;
  undefined4 *local_9c;
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00421ed1;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  if ((int)param_1 < 0) {
    *(undefined4 *)((int)this + 0x20) = 0;
    (**(code **)(*(int *)(*(int *)((int)this + 0x1c4) + 0x6a0) + 0xc))(0xffffffff,0);
    (**(code **)(**(int **)((int)this + 0x1c4) + 0x2c))(&DAT_0042628c);
    DuiLib::CControlUI::Invalidate(*(CControlUI **)((int)this + 0x1c4));
    FUN_0040b9e0(this,*(int *)((int)this + 0x20));
    puVar5 = (undefined4 *)((int)this + 0x3a8);
    iVar4 = 0x1e;
    do {
      (**(code **)(*(int *)puVar5[0x5a] + 0x2c))(&DAT_00427814);
      (**(code **)(*(int *)*puVar5 + 0x2c))(&DAT_00427814);
      (**(code **)(*(int *)puVar5[-0x5a] + 0x2c))(&DAT_00427c1c);
      puVar5 = puVar5 + 1;
      iVar4 = iVar4 + -1;
    } while (iVar4 != 0);
    (**(code **)(**(int **)((int)this + 0x1c0) + 0x2c))(&DAT_0042628c);
    *(undefined4 *)((int)this + 0x1c) = 0;
  }
  else {
    if (DAT_0046c398 == DAT_0046c39c) {
      *(undefined4 *)((int)this + 0x1c) = 0;
    }
    else {
      if ((uint)(DAT_0046c39c - DAT_0046c398 >> 2) <= param_1) {
                    /* WARNING: Subroutine does not return */
        FUN_004050f0();
      }
      iVar4 = *(int *)(DAT_0046c398 + param_1 * 4);
      *(int *)((int)this + 0x1c) = iVar4;
      if ((iVar4 != 0) && (*(int *)(iVar4 + 0xcc) == 0)) {
        uVar2 = (uint)*(byte *)(iVar4 + 200);
        *(uint *)((int)this + 0x20) = uVar2;
        if (uVar2 == 0) {
          (**(code **)(**(int **)((int)this + 0x1c4) + 0x2c))(&DAT_0042628c,local_14);
          uVar2 = *(uint *)((int)this + 0x20);
        }
        FUN_0040b9e0(this,uVar2);
        DuiLib::CDuiString::CDuiString(local_98);
        local_8 = 0;
        local_a0 = 0x1e;
        local_9c = (undefined4 *)((int)this + 0x3a8);
        puVar5 = (undefined4 *)((int)this + 0x2c);
        do {
          this_00 = (CDuiString *)((-0x2c - (int)this) + (int)puVar5);
          uVar1 = *(undefined4 *)(*(int *)((int)this + 0x1c) + (0xac - (int)this) + (int)puVar5);
          puVar5[-1] = uVar1;
          *puVar5 = *(undefined4 *)(this_00 + *(int *)((int)this + 0x1c) + 0xdc);
          *(undefined2 *)((int)puVar5 + 6) =
               *(undefined2 *)(this_00 + *(int *)((int)this + 0x1c) + 0xe2);
          DuiLib::CDuiString::Format(this_00,(wchar_t *)local_98,&DAT_00424f54,uVar1);
          iVar4 = *(int *)local_9c[0x5a];
          pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
          (**(code **)(iVar4 + 0x2c))(pwVar3);
          DuiLib::CDuiString::Format(this_01,(wchar_t *)local_98,&DAT_00424f54,*puVar5);
          iVar4 = *(int *)*local_9c;
          pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
          (**(code **)(iVar4 + 0x2c))(pwVar3);
          DuiLib::CDuiString::Format
                    (this_02,(wchar_t *)local_98,&DAT_00424f54,(uint)*(ushort *)((int)puVar5 + 6));
          iVar4 = *(int *)local_9c[-0x5a];
          pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
          (**(code **)(iVar4 + 0x2c))(pwVar3);
          puVar5 = puVar5 + 3;
          local_9c = local_9c + 1;
          local_a0 = local_a0 + -1;
        } while (local_a0 != 0);
        (**(code **)(*(int *)(*(int *)((int)this + 0x1c4) + 0x6a0) + 0xc))
                  (*(int *)((int)this + 0x20) + -1,0);
        (**(code **)(**(int **)((int)this + 0x1c0) + 0x2c))(*(int *)((int)this + 0x1c) + 100);
        DuiLib::CDuiString::~CDuiString(local_98);
        ExceptionList = local_10;
        return;
      }
    }
    *(undefined4 *)((int)this + 0x20) = 0;
    (**(code **)(*(int *)(*(int *)((int)this + 0x1c4) + 0x6a0) + 0xc))(0xffffffff,0);
    (**(code **)(**(int **)((int)this + 0x1c4) + 0x2c))(&DAT_0042628c);
    FUN_0040b9e0(this,*(int *)((int)this + 0x20));
    puVar5 = (undefined4 *)((int)this + 0x3a8);
    iVar4 = 0x1e;
    do {
      (**(code **)(*(int *)puVar5[0x5a] + 0x2c))(&DAT_00427814);
      (**(code **)(*(int *)*puVar5 + 0x2c))(&DAT_00427814);
      (**(code **)(*(int *)puVar5[-0x5a] + 0x2c))(&DAT_00427c1c);
      puVar5 = puVar5 + 1;
      iVar4 = iVar4 + -1;
    } while (iVar4 != 0);
    (**(code **)(**(int **)((int)this + 0x1c0) + 0x2c))(&DAT_0042628c);
  }
  ExceptionList = local_10;
  return;
}


