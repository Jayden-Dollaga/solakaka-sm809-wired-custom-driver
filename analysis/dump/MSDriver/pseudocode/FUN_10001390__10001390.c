// Program: MSDriver.dll
// Function: FUN_10001390
// Entry: 10001390
// Body: 10001390 - 10001442
// Signature: undefined4 FUN_10001390(undefined4 param_1)


undefined4 __cdecl FUN_10001390(undefined4 param_1)

{
  int iVar1;
  int *piVar2;
  int *piVar3;
  
  switch(param_1) {
  case 2:
  case 6:
  case 7:
  case 0x12:
    DAT_10009ed0 = 1;
    DAT_10009ecc = 0;
    Open_DevMonitor(DAT_10009ec8,DAT_10009ec0,DAT_10009ec4);
    DAT_10009ed0 = 0;
    break;
  case 4:
    DAT_10009ecc = 1;
    if (DAT_10009edc != 2) {
      if (DAT_1000c00c != 0) {
        DAT_10009ee0 = 1;
        piVar3 = DAT_10009eb8;
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
      return 0;
    }
  }
  return 0;
}


