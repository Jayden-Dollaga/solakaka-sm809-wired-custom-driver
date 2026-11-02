// Program: SM809 mouse Software.exe
// Function: FUN_004111b0
// Entry: 004111b0
// Body: 004111b0 - 0041121d
// Signature: undefined FUN_004111b0(void * this, undefined4 param_1, undefined4 param_2, undefined4 param_3, undefined4 param_4)


void __thiscall
FUN_004111b0(void *this,undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined4 *puVar1;
  int iVar2;
  int iVar3;
  
  iVar2 = *(int *)((int)this + 0x2a4);
  if (iVar2 < 0x28) {
    iVar3 = iVar2;
    if (*(int *)((int)this + 0x2b4) != -1) {
      iVar3 = *(int *)((int)this + 0x2b4);
    }
    if (iVar3 < iVar2) {
      puVar1 = (undefined4 *)(iVar2 * 0x10 + 0x24 + (int)this);
      do {
        iVar2 = iVar2 + -1;
        *puVar1 = puVar1[-4];
        puVar1[1] = puVar1[-3];
        puVar1[2] = puVar1[-2];
        puVar1[3] = puVar1[-1];
        puVar1 = puVar1 + -4;
      } while (iVar3 < iVar2);
    }
    puVar1 = (undefined4 *)((int)this + iVar3 * 0x10 + 0x24);
    *puVar1 = param_1;
    puVar1[1] = param_2;
    puVar1[2] = param_3;
    puVar1[3] = param_4;
    *(int *)((int)this + 0x2a4) = *(int *)((int)this + 0x2a4) + 1;
    *(int *)((int)this + 700) = *(int *)((int)this + 700) + 1;
    if (*(int *)((int)this + 0x2b4) != -1) {
      *(int *)((int)this + 0x2b4) = *(int *)((int)this + 0x2b4) + 1;
    }
  }
  return;
}


