// Program: Hook.dll
// Function: FUN_10005145
// Entry: 10005145
// Body: 10005145 - 10005175
// Signature: undefined4 FUN_10005145(FILE * param_1)


undefined4 __cdecl FUN_10005145(FILE *param_1)

{
  undefined4 uVar1;
  
  uVar1 = 0xffffffff;
  if ((param_1->_flag & 0x40) == 0) {
    FUN_10002f1d((uint)param_1);
    uVar1 = __fclose_lk(param_1);
    FUN_10002f6f((uint)param_1);
  }
  else {
    param_1->_flag = 0;
  }
  return uVar1;
}


