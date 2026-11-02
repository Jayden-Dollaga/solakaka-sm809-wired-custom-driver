// Program: MSDriver.dll
// Function: FUN_100022da
// Entry: 100022da
// Body: 100022da - 10002321
// Signature: undefined FUN_100022da(LPVOID param_1)


void __cdecl FUN_100022da(LPVOID param_1)

{
  uint *puVar1;
  
  if (param_1 != (LPVOID)0x0) {
    FUN_1000277c(9);
    puVar1 = (uint *)FUN_10002830((int)param_1);
    if (puVar1 != (uint *)0x0) {
      FUN_1000285b(puVar1,(uint)param_1);
      FUN_100027dd(9);
      return;
    }
    FUN_100027dd(9);
    HeapFree(DAT_1000b5f0,0,param_1);
  }
  return;
}


