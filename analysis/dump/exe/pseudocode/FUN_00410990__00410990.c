// Program: SM809 mouse Software.exe
// Function: FUN_00410990
// Entry: 00410990
// Body: 00410990 - 00410b78
// Signature: undefined FUN_00410990(void * this, uint param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_00410990(void *this,uint param_1)

{
  ushort uVar1;
  uint uVar2;
  int iVar3;
  wchar_t *pwVar4;
  int iVar5;
  CDuiString *this_00;
  undefined4 *puVar6;
  undefined4 *puVar7;
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00421761;
  local_10 = ExceptionList;
  uVar2 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  *(undefined4 *)((int)this + 0x2c0) = 0;
  local_14 = uVar2;
  if ((int)param_1 < 0) {
    memset((void *)((int)this + 0x24),0,0x280);
    *(undefined4 *)((int)this + 0x2a4) = 0;
    *(undefined4 *)((int)this + 700) = 0xffffffff;
    FUN_00411740(this,-1);
    (**(code **)(**(int **)((int)this + 0x348) + 0x2c))(&DAT_0042628c,uVar2);
    (**(code **)(**(int **)((int)this + 0x388) + 0x2c))(&DAT_00427820);
    *(undefined4 *)((int)this + 0x1c) = 0;
  }
  else {
    if (DAT_0046c380 == DAT_0046c384) {
      iVar3 = 0;
    }
    else {
      if ((uint)(DAT_0046c384 - DAT_0046c380 >> 2) <= param_1) {
                    /* WARNING: Subroutine does not return */
        FUN_004050f0();
      }
      iVar3 = *(int *)(DAT_0046c380 + param_1 * 4);
    }
    *(int *)((int)this + 0x1c) = iVar3;
    if (*(int *)(iVar3 + 0xd0) == 1) {
      memset((undefined4 *)((int)this + 0x24),0,0x280);
      *(undefined4 *)((int)this + 0x2a4) = 0;
      *(undefined4 *)((int)this + 700) = 0xffffffff;
      FUN_00411740(this,-1);
      (**(code **)(**(int **)((int)this + 0x348) + 0x2c))(&DAT_0042628c);
      (**(code **)(**(int **)((int)this + 0x388) + 0x2c))(&DAT_00427820);
    }
    else {
      puVar6 = (undefined4 *)(iVar3 + 0xd8);
      puVar7 = (undefined4 *)((int)this + 0x24);
      for (iVar5 = 0xa0; iVar5 != 0; iVar5 = iVar5 + -1) {
        *puVar7 = *puVar6;
        puVar6 = puVar6 + 1;
        puVar7 = puVar7 + 1;
      }
      uVar1 = *(ushort *)(iVar3 + 0xcc);
      *(uint *)((int)this + 0x2a4) = (uint)uVar1;
      *(uint *)((int)this + 0x2f4) = (uint)*(ushort *)(iVar3 + 200);
      if (uVar1 == 0) {
        *(undefined4 *)((int)this + 700) = 0xffffffff;
        FUN_00411740(this,-1);
      }
      DuiLib::CDuiString::CDuiString(local_98);
      local_8 = 0;
      DuiLib::CDuiString::Format
                (this_00,(wchar_t *)local_98,&DAT_00424f54,*(undefined4 *)((int)this + 0x2f4));
      iVar3 = **(int **)((int)this + 0x388);
      pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
      (**(code **)(iVar3 + 0x2c))(pwVar4);
      local_8 = 0xffffffff;
      DuiLib::CDuiString::~CDuiString(local_98);
    }
  }
  FUN_00411220((int)this);
  ExceptionList = local_10;
  return;
}


