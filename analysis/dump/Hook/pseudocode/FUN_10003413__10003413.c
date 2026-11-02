// Program: Hook.dll
// Function: FUN_10003413
// Entry: 10003413
// Body: 10003413 - 10003460
// Signature: int * FUN_10003413(uint * param_1)


int * __cdecl FUN_10003413(uint *param_1)

{
  int *piVar1;
  
  if (param_1 <= DAT_10007840) {
    FUN_1000328a(9);
    piVar1 = FUN_10004029(param_1);
    FUN_100032eb(9);
    if (piVar1 != (int *)0x0) {
      return piVar1;
    }
  }
  if (param_1 == (uint *)0x0) {
    param_1 = (uint *)0x1;
  }
  piVar1 = HeapAlloc(DAT_100092e4,0,(int)param_1 + 0xfU & 0xfffffff0);
  return piVar1;
}


