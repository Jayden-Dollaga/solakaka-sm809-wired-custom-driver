// Program: SM809 mouse Software.exe
// Function: FUN_0040f6e0
// Entry: 0040f6e0
// Body: 0040f6e0 - 0040f728
// Signature: undefined FUN_0040f6e0(void * this, int param_1)


void __thiscall FUN_0040f6e0(void *this,int param_1)

{
  int iVar1;
  
  iVar1 = *(int *)(param_1 + 0x108);
  if (iVar1 == *(int *)((int)this + 0x34c)) {
    *(undefined4 *)((int)this + 0x20) = 0;
    iVar1 = *(int *)(param_1 + 0x108);
  }
  if (iVar1 == *(int *)((int)this + 0x350)) {
    *(undefined4 *)((int)this + 0x20) = 1;
    iVar1 = *(int *)(param_1 + 0x108);
  }
  if (iVar1 == *(int *)((int)this + 0x354)) {
    *(undefined4 *)((int)this + 0x20) = 2;
  }
  return;
}


