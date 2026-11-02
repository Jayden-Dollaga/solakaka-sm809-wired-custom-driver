// Program: SM809 mouse Software.exe
// Function: FUN_00406c10
// Entry: 00406c10
// Body: 00406c10 - 00406c54
// Signature: undefined FUN_00406c10(void * this, int param_1)


void __thiscall FUN_00406c10(void *this,int param_1)

{
  int iVar1;
  int *piVar2;
  
  iVar1 = 0;
  piVar2 = (int *)((int)this + 0x120);
  do {
    if (*(int *)(param_1 + 0x108) == *piVar2) {
      *(int *)(DAT_00432aa0 + 0x14c) = iVar1;
      FUN_00408bc0(this,iVar1);
      return;
    }
    iVar1 = iVar1 + 1;
    piVar2 = piVar2 + 1;
  } while (iVar1 < 2);
  return;
}


