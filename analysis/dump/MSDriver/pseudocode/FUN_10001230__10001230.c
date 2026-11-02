// Program: MSDriver.dll
// Function: FUN_10001230
// Entry: 10001230
// Body: 10001230 - 10001386
// Signature: undefined4 FUN_10001230(int param_1, int param_2)


undefined4 __cdecl FUN_10001230(int param_1,int param_2)

{
  int *piVar1;
  int *piVar2;
  undefined4 *puVar3;
  uint uVar4;
  undefined2 extraout_var;
  int iVar5;
  undefined4 *puVar6;
  
  if (param_1 == 0x8000) {
    OutputDebugStringA(s_DBT_DEVICEARRIVAL__10009064);
    if (((DAT_10009ecc == 0) && (*(int *)(param_2 + 4) == 5)) &&
       (puVar3 = _malloc(0xac), puVar3 != (undefined4 *)0x0)) {
      puVar6 = puVar3;
      for (iVar5 = 0x2b; iVar5 != 0; iVar5 = iVar5 + -1) {
        *puVar6 = 0;
        puVar6 = puVar6 + 1;
      }
      uVar4 = FUN_10001c00((LPCSTR)(param_2 + 0x1c),puVar3 + 3,0);
      if ((char)uVar4 == '\x01') {
        FUN_100014b0(puVar3);
        OutputDebugStringA(s_DBT_DEVICEARRIVAL_finished__10009044);
        return 0;
      }
      FUN_100022da(puVar3);
    }
  }
  else if (((param_1 == 0x8004) &&
           (OutputDebugStringA(s_DBT_DEVICEREMOVECOMPLETE_1000909c), *(int *)(param_2 + 4) == 6)) &&
          ((int **)DAT_10009eb8 != &DAT_10009eb8)) {
    iVar5 = DAT_10009eb8[3];
    piVar1 = DAT_10009eb8;
    while (iVar5 != *(int *)(param_2 + 0xc)) {
      piVar1 = (int *)*piVar1;
      if ((int **)piVar1 == &DAT_10009eb8) {
        return 0;
      }
      iVar5 = piVar1[3];
    }
    if ((int **)piVar1 != &DAT_10009eb8) {
      FUN_10001640((int)piVar1);
      PostMessageA(DAT_1000c000,0x5f5,0,piVar1[0x28]);
      FUN_10001470(0,CONCAT22(extraout_var,(short)piVar1[2]));
      FUN_10001f90(piVar1 + 3);
      piVar2 = (int *)piVar1[1];
      iVar5 = *piVar1;
      *piVar2 = iVar5;
      *(int **)(iVar5 + 4) = piVar2;
      FUN_100022da(piVar1);
      DAT_10009030 = 1;
      OutputDebugStringA(s_DBT_DEVICEREMOVECOMPLETE_finishe_10009078);
      return 0;
    }
  }
  return 0;
}


