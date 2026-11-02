// Program: SM809 mouse Software.exe
// Function: FUN_0040e460
// Entry: 0040e460
// Body: 0040e460 - 0040e4c7
// Signature: undefined FUN_0040e460(void * this, int param_1)


void __thiscall FUN_0040e460(void *this,int param_1)

{
  int *piVar1;
  int iVar2;
  
  iVar2 = 0;
  piVar1 = (int *)((int)this + 0x1c);
  do {
    if (*(int *)(param_1 + 0x108) == *piVar1) {
      *(int *)(DAT_00432aa0 + 0xf0) = iVar2;
      FUN_0040eaf0(this,iVar2);
      break;
    }
    iVar2 = iVar2 + 1;
    piVar1 = piVar1 + 1;
  } while (iVar2 < 0xc);
  piVar1 = (int *)((int)this + 0x94);
  iVar2 = 0;
  do {
    if (*(int *)(param_1 + 0x108) == *piVar1) {
      *(int *)(DAT_00432aa0 + 0xfc) = iVar2;
      return;
    }
    iVar2 = iVar2 + 1;
    piVar1 = piVar1 + 1;
  } while (iVar2 < 2);
  return;
}


