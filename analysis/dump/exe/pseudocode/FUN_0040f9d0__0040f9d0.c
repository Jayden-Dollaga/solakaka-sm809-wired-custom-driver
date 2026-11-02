// Program: SM809 mouse Software.exe
// Function: FUN_0040f9d0
// Entry: 0040f9d0
// Body: 0040f9d0 - 0040fa75
// Signature: undefined FUN_0040f9d0(void * this, int param_1)


void __thiscall FUN_0040f9d0(void *this,int param_1)

{
  int iVar1;
  int iVar2;
  
  if (*(CCheckBoxUI **)(param_1 + 0x108) == *(CCheckBoxUI **)((int)this + 0x35c)) {
    if (((*(int *)((int)this + 0x1c) == 0) || (*(int *)(*(int *)((int)this + 0x1c) + 0xd0) == 1)) ||
       (0x27 < *(int *)((int)this + 0x2a4))) {
                    /* WARNING: Could not recover jumptable at 0x0040fa70. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      DuiLib::CCheckBoxUI::SetCheck(*(CCheckBoxUI **)((int)this + 0x35c),false);
      return;
    }
    if (*(int *)((int)this + 0x2a8) != 0) {
      FUN_00410ca0((int)this);
      return;
    }
    iVar1 = *(int *)((int)this + 700);
    if (-1 < iVar1) {
      iVar2 = iVar1 + 1;
    }
    else {
      *(undefined4 *)((int)this + 0x2a4) = 0;
      memset((void *)((int)this + 0x24),0,0x280);
      iVar2 = -1;
    }
    *(int *)((int)this + 0x2b0) = iVar2;
    *(int *)((int)this + 0x2b4) = iVar2;
    *(uint *)((int)this + 0x2c0) = (uint)(-1 < iVar1);
    FUN_00410b80((int)this);
  }
  return;
}


