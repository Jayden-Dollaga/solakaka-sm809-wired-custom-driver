// Program: SM809 mouse Software.exe
// Function: FUN_00405ce0
// Entry: 00405ce0
// Body: 00405ce0 - 00405cf7
// Signature: undefined4 * FUN_00405ce0(undefined4 * param_1)


undefined4 * __fastcall FUN_00405ce0(undefined4 *param_1)

{
  *(undefined8 *)(param_1 + 1) = 0;
  param_1[1] = "bad array new length";
  *param_1 = std::bad_array_new_length::vftable;
  return param_1;
}


