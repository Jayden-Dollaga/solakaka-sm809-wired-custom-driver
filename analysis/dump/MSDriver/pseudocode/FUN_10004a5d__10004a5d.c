// Program: MSDriver.dll
// Function: FUN_10004a5d
// Entry: 10004a5d
// Body: 10004a5d - 10004aa0
// Signature: undefined FUN_10004a5d(undefined4 * param_1)


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __cdecl FUN_10004a5d(undefined4 *param_1)

{
  void *pvVar1;
  
  _DAT_1000a0c8 = _DAT_1000a0c8 + 1;
  pvVar1 = _malloc(0x1000);
  param_1[2] = pvVar1;
  if (pvVar1 == (void *)0x0) {
    param_1[3] = param_1[3] | 4;
    param_1[2] = param_1 + 5;
    param_1[6] = 2;
  }
  else {
    param_1[3] = param_1[3] | 8;
    param_1[6] = 0x1000;
  }
  param_1[1] = 0;
  *param_1 = param_1[2];
  return;
}


