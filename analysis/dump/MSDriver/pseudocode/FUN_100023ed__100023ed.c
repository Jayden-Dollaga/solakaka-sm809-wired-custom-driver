// Program: MSDriver.dll
// Function: FUN_100023ed
// Entry: 100023ed
// Body: 100023ed - 1000243a
// Signature: int * FUN_100023ed(uint * param_1)


int * __cdecl FUN_100023ed(uint *param_1)

{
  int *piVar1;
  
  if (param_1 <= DAT_1000920c) {
    FUN_1000277c(9);
    piVar1 = FUN_10002b86(param_1);
    FUN_100027dd(9);
    if (piVar1 != (int *)0x0) {
      return piVar1;
    }
  }
  if (param_1 == (uint *)0x0) {
    param_1 = (uint *)0x1;
  }
  piVar1 = HeapAlloc(DAT_1000b5f0,0,(int)param_1 + 0xfU & 0xfffffff0);
  return piVar1;
}


