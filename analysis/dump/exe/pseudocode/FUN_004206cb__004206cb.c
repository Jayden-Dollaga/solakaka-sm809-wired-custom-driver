// Program: SM809 mouse Software.exe
// Function: FUN_004206cb
// Entry: 004206cb
// Body: 004206cb - 004206e2
// Signature: undefined4 * FUN_004206cb(undefined4 * param_1)


undefined4 * __fastcall FUN_004206cb(undefined4 *param_1)

{
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[1] = "bad allocation";
  *param_1 = std::bad_alloc::vftable;
  return param_1;
}


