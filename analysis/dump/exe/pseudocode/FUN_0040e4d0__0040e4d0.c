// Program: SM809 mouse Software.exe
// Function: FUN_0040e4d0
// Entry: 0040e4d0
// Body: 0040e4d0 - 0040e52e
// Signature: undefined FUN_0040e4d0(void * this, int param_1)


void __thiscall FUN_0040e4d0(void *this,int param_1)

{
  int iVar1;
  
  iVar1 = *(int *)(param_1 + 0x108);
  if (iVar1 == *(int *)((int)this + 0x54)) {
    *(undefined4 *)(DAT_00432aa0 + 0xf4) = *(undefined4 *)(param_1 + 0x118);
    return;
  }
  if (iVar1 == *(int *)((int)this + 0x58)) {
    *(undefined4 *)(DAT_00432aa0 + 0xf8) = *(undefined4 *)(param_1 + 0x118);
    return;
  }
  if (iVar1 == *(int *)((int)this + 0xa4)) {
    *(undefined4 *)(DAT_00432aa0 + 0x100) = *(undefined4 *)(param_1 + 0x118);
  }
  return;
}


