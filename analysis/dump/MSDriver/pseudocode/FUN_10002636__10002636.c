// Program: MSDriver.dll
// Function: FUN_10002636
// Entry: 10002636
// Body: 10002636 - 10002671
// Signature: undefined4 FUN_10002636(int param_1)


undefined4 __cdecl FUN_10002636(int param_1)

{
  int iVar1;
  
  DAT_1000b5f0 = HeapCreate((uint)(param_1 == 0),0x1000,0);
  if (DAT_1000b5f0 != (HANDLE)0x0) {
    iVar1 = FUN_100027f2();
    if (iVar1 != 0) {
      return 1;
    }
    HeapDestroy(DAT_1000b5f0);
  }
  return 0;
}


