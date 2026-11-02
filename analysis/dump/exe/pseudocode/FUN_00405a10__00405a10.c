// Program: SM809 mouse Software.exe
// Function: FUN_00405a10
// Entry: 00405a10
// Body: 00405a10 - 00405a28
// Signature: undefined FUN_00405a10(int param_1)


void __fastcall FUN_00405a10(int param_1)

{
  undefined4 *puVar1;
  
  if (*(int **)(param_1 + 4) != (int *)0x0) {
    puVar1 = (undefined4 *)(**(code **)(**(int **)(param_1 + 4) + 8))();
    if (puVar1 != (undefined4 *)0x0) {
      (**(code **)*puVar1)(1);
    }
  }
  return;
}


