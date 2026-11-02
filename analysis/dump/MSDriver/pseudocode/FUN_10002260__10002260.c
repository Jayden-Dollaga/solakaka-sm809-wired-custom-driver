// Program: MSDriver.dll
// Function: FUN_10002260
// Entry: 10002260
// Body: 10002260 - 100022a8
// Signature: undefined FUN_10002260(int param_1)


void __cdecl FUN_10002260(int param_1)

{
  int *piVar1;
  
  *(undefined4 *)(param_1 + 0x90) = 0;
  if (*(ushort *)(param_1 + 0xc) != 0) {
    piVar1 = FUN_10002322((uint)*(ushort *)(param_1 + 0xc),1);
    *(int **)(param_1 + 0x54) = piVar1;
  }
  if (*(ushort *)(param_1 + 0xe) != 0) {
    piVar1 = FUN_10002322((uint)*(ushort *)(param_1 + 0xe),1);
    *(int **)(param_1 + 0x68) = piVar1;
  }
  return;
}


