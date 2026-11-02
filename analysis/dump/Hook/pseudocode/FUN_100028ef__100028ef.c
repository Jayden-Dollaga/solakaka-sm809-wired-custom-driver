// Program: Hook.dll
// Function: FUN_100028ef
// Entry: 100028ef
// Body: 100028ef - 1000292a
// Signature: undefined4 FUN_100028ef(int param_1)


undefined4 __cdecl FUN_100028ef(int param_1)

{
  int iVar1;
  
  DAT_100092e4 = HeapCreate((uint)(param_1 == 0),0x1000,0);
  if (DAT_100092e4 != (HANDLE)0x0) {
    iVar1 = FUN_10003c95();
    if (iVar1 != 0) {
      return 1;
    }
    HeapDestroy(DAT_100092e4);
  }
  return 0;
}


