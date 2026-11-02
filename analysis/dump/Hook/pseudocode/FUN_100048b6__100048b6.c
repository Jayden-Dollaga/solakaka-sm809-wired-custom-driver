// Program: Hook.dll
// Function: FUN_100048b6
// Entry: 100048b6
// Body: 100048b6 - 100048e3
// Signature: int FUN_100048b6(int * param_1)


int __cdecl FUN_100048b6(int *param_1)

{
  int iVar1;
  
  iVar1 = FUN_100048e4(param_1);
  if (iVar1 != 0) {
    return -1;
  }
  if ((*(byte *)((int)param_1 + 0xd) & 0x40) == 0) {
    return 0;
  }
  iVar1 = FUN_100051c2(param_1[4]);
  return -(uint)(iVar1 != 0);
}


