// Program: Hook.dll
// Function: FUN_10002df4
// Entry: 10002df4
// Body: 10002df4 - 10002e37
// Signature: undefined FUN_10002df4(undefined4 * param_1)


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __cdecl FUN_10002df4(undefined4 *param_1)

{
  void *pvVar1;
  
  _DAT_10007e94 = _DAT_10007e94 + 1;
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


