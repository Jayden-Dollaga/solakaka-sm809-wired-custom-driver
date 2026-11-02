// Program: Hook.dll
// Function: FUN_10002101
// Entry: 10002101
// Body: 10002101 - 1000211a
// Signature: undefined FUN_10002101(undefined4 * param_1, undefined4 * param_2)


void __cdecl FUN_10002101(undefined4 *param_1,undefined4 *param_2)

{
  for (; param_1 < param_2; param_1 = param_1 + 1) {
    if ((code *)*param_1 != (code *)0x0) {
      (*(code *)*param_1)();
    }
  }
  return;
}


