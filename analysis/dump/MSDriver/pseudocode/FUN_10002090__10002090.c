// Program: MSDriver.dll
// Function: FUN_10002090
// Entry: 10002090
// Body: 10002090 - 10002104
// Signature: undefined FUN_10002090(int * param_1)


void __cdecl FUN_10002090(int *param_1)

{
  int *piVar1;
  int iVar2;
  
  if (param_1[0x28] != 0) {
    PostMessageA(DAT_1000c000,0x5f5,0,param_1[0x28]);
  }
  if (DAT_10009ee0 == 0) {
    FUN_10001470(0,(uint)*(ushort *)(param_1 + 2));
  }
  else {
    DAT_10009ee0 = 0;
  }
  FUN_10001640((int)param_1);
  FUN_10001f90(param_1 + 3);
  piVar1 = (int *)param_1[1];
  iVar2 = *param_1;
  *piVar1 = iVar2;
  *(int **)(iVar2 + 4) = piVar1;
  FUN_100022da(param_1);
  return;
}


