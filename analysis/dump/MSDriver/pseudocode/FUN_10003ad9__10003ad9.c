// Program: MSDriver.dll
// Function: FUN_10003ad9
// Entry: 10003ad9
// Body: 10003ad9 - 10003af2
// Signature: undefined FUN_10003ad9(undefined4 * param_1, undefined4 * param_2)


void __cdecl FUN_10003ad9(undefined4 *param_1,undefined4 *param_2)

{
  for (; param_1 < param_2; param_1 = param_1 + 1) {
    if ((code *)*param_1 != (code *)0x0) {
      (*(code *)*param_1)();
    }
  }
  return;
}


