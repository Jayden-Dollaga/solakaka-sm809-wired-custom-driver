// Program: MSDriver.dll
// Function: FUN_10001b90
// Entry: 10001b90
// Body: 10001b90 - 10001bf5
// Signature: undefined FUN_10001b90(void)


void FUN_10001b90(void)

{
  int iVar1;
  int *piVar2;
  int *piVar3;
  
  piVar3 = DAT_10009eb8;
  if (DAT_1000c00c != 0) {
    while (DAT_10009eb8 = piVar3, (int **)piVar3 != &DAT_10009eb8) {
      iVar1 = *piVar3;
      piVar2 = (int *)piVar3[1];
      *piVar2 = iVar1;
      *(int **)(iVar1 + 4) = piVar2;
      FUN_10002090(piVar3);
      piVar3 = DAT_10009eb8;
    }
  }
  DAT_10009030 = 1;
  if (DAT_1000c00c != 0) {
    SendMessageA(DAT_1000c000,0x10,0,0);
  }
  DAT_1000c00c = 0;
  return;
}


