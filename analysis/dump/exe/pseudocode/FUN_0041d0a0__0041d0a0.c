// Program: SM809 mouse Software.exe
// Function: FUN_0041d0a0
// Entry: 0041d0a0
// Body: 0041d0a0 - 0041d10e
// Signature: undefined FUN_0041d0a0(void * this, int param_1)


void __thiscall FUN_0041d0a0(void *this,int param_1)

{
  int iVar1;
  
  iVar1 = DAT_00432aa0;
  if (*(int *)(param_1 + 0x108) == *(int *)((int)this + 0x134)) {
    *(char *)(DAT_00432aa0 + 0x139) = *(char *)(param_1 + 0x118) + '\x01';
    if (*(int *)(param_1 + 0x118) < *(int *)(iVar1 + 0x84)) {
      *(int *)(iVar1 + 0x84) = *(int *)(param_1 + 0x118);
      (**(code **)(**(int **)((int)this + *(int *)(param_1 + 0x118) * 4 + 0x28) + 0x1bc))(1,1);
      iVar1 = DAT_00432aa0;
    }
    FUN_0041d620(this,(uint)*(byte *)(iVar1 + 0x139));
  }
  return;
}


