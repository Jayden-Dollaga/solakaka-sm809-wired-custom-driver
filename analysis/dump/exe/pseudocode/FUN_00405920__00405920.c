// Program: SM809 mouse Software.exe
// Function: FUN_00405920
// Entry: 00405920
// Body: 00405920 - 00405937
// Signature: undefined4 * FUN_00405920(undefined4 * param_1)


undefined4 * __fastcall FUN_00405920(undefined4 *param_1)

{
  *(undefined8 *)(param_1 + 1) = 0;
  param_1[1] = "bad cast";
  *param_1 = std::bad_cast::vftable;
  return param_1;
}


