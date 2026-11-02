// Program: SM809 mouse Software.exe
// Function: FUN_004176f0
// Entry: 004176f0
// Body: 004176f0 - 004178da
// Signature: undefined FUN_004176f0(void * this, CDuiString * param_1)


void __thiscall FUN_004176f0(void *this,CDuiString *param_1)

{
  int iVar1;
  bool bVar2;
  
  bVar2 = DuiLib::CDuiString::IsEmpty(param_1 + 0x84);
  if (!bVar2) {
    DuiLib::WindowImplBase::Notify(this,(tagTNotifyUI *)param_1);
    return;
  }
  bVar2 = DuiLib::CDuiString::operator==(param_1,L"click");
  if (bVar2) {
    (**(code **)(*(int *)((int)this + -0x20) + 0x20))(param_1);
    return;
  }
  bVar2 = DuiLib::CDuiString::operator==(param_1,L"selectchanged");
  if (bVar2) {
    iVar1 = *(int *)(param_1 + 0x108);
    if (iVar1 == *(int *)((int)this + 0x16c8)) {
      (**(code **)(**(int **)((int)this + 0x16f8) + 0x204))(0);
                    /* WARNING: Could not recover jumptable at 0x00417780. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(**(int **)((int)this + 0x16fc) + 0x204))();
      return;
    }
    if (iVar1 == *(int *)((int)this + 0x16cc)) {
      (**(code **)(**(int **)((int)this + 0x16f8) + 0x204))(0);
                    /* WARNING: Could not recover jumptable at 0x004177b1. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(**(int **)((int)this + 0x16fc) + 0x204))();
      return;
    }
    if (iVar1 == *(int *)((int)this + 0x16d0)) {
      (**(code **)(**(int **)((int)this + 0x16f8) + 0x204))(0);
                    /* WARNING: Could not recover jumptable at 0x004177e2. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(**(int **)((int)this + 0x16fc) + 0x204))();
      return;
    }
    if (iVar1 == *(int *)((int)this + 0x16d4)) {
                    /* WARNING: Could not recover jumptable at 0x00417803. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(**(int **)((int)this + 0x16f8) + 0x204))();
      return;
    }
    if (iVar1 == *(int *)((int)this + 0x16d8)) {
                    /* WARNING: Could not recover jumptable at 0x00417828. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(**(int **)((int)this + 0x16f8) + 0x204))();
      return;
    }
  }
  else {
    bVar2 = DuiLib::CDuiString::operator==(param_1,L"itemselect");
    if (bVar2) {
      if ((*(int *)(param_1 + 0x108) == *(int *)((int)this + 0x16dc)) &&
         ((DAT_00432aa8 != *(uint *)(param_1 + 0x118) || (*(int *)((int)this + 0x1560) == 1)))) {
        *(undefined4 *)((int)this + 0x1560) = 0;
        DAT_00432aa8 = *(uint *)(param_1 + 0x118);
        if (DAT_0046c38c == DAT_0046c390) {
          DAT_00432aa0 = 0;
        }
        else {
          if ((uint)(DAT_0046c390 - DAT_0046c38c >> 2) <= DAT_00432aa8) {
                    /* WARNING: Subroutine does not return */
            FUN_004050f0();
          }
          DAT_00432aa0 = *(undefined4 *)(DAT_0046c38c + DAT_00432aa8 * 4);
        }
        (**(code **)(**(int **)((int)this + 0x16ec) + 0x2c))(DAT_00432aa0);
        FUN_00417540((int)this + -0x20);
        return;
      }
    }
    else {
      bVar2 = DuiLib::CDuiString::operator==(param_1,L"killfocus");
      if (bVar2) {
        FUN_00417d10((void *)((int)this + -0x20),(int)param_1);
      }
    }
  }
  return;
}


