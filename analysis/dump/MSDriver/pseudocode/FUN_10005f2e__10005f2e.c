// Program: MSDriver.dll
// Function: FUN_10005f2e
// Entry: 10005f2e
// Body: 10005f2e - 10005f5e
// Signature: undefined4 FUN_10005f2e(FILE * param_1)


undefined4 __cdecl FUN_10005f2e(FILE *param_1)

{
  undefined4 uVar1;
  
  uVar1 = 0xffffffff;
  if ((param_1->_flag & 0x40) == 0) {
    FUN_10004b86((uint)param_1);
    uVar1 = __fclose_lk(param_1);
    FUN_10004bd8((uint)param_1);
  }
  else {
    param_1->_flag = 0;
  }
  return uVar1;
}


