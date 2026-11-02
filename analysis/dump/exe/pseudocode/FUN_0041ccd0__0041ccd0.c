// Program: SM809 mouse Software.exe
// Function: FUN_0041ccd0
// Entry: 0041ccd0
// Body: 0041ccd0 - 0041cd30
// Signature: undefined FUN_0041ccd0(void * this, int param_1)


void __thiscall FUN_0041ccd0(void *this,int param_1)

{
  int iVar1;
  int iVar2;
  int *piVar3;
  
  iVar1 = DAT_00432aa0;
  piVar3 = (int *)((int)this + 0x18);
  iVar2 = 0;
  do {
    if (*(int *)(param_1 + 0x108) == *piVar3) {
      *(int *)(DAT_00432aa0 + 0x80) = iVar2;
      break;
    }
    iVar2 = iVar2 + 1;
    piVar3 = piVar3 + 1;
  } while (iVar2 < 4);
  iVar2 = 0;
  piVar3 = (int *)((int)this + 0x28);
  do {
    if (*(int *)(param_1 + 0x108) == *piVar3) {
      *(int *)(iVar1 + 0x84) = iVar2;
      return;
    }
    iVar2 = iVar2 + 1;
    piVar3 = piVar3 + 1;
  } while (iVar2 < 8);
  return;
}


