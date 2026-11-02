// Program: MSDriver.dll
// Function: FUN_10005a56
// Entry: 10005a56
// Body: 10005a56 - 10005a83
// Signature: int FUN_10005a56(int * param_1)


int __cdecl FUN_10005a56(int *param_1)

{
  int iVar1;
  
  iVar1 = FUN_10005a84(param_1);
  if (iVar1 != 0) {
    return -1;
  }
  if ((*(byte *)((int)param_1 + 0xd) & 0x40) == 0) {
    return 0;
  }
  iVar1 = FUN_10005fab(param_1[4]);
  return -(uint)(iVar1 != 0);
}


