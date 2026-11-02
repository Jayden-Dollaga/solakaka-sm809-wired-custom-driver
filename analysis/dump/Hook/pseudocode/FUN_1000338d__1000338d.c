// Program: Hook.dll
// Function: FUN_1000338d
// Entry: 1000338d
// Body: 1000338d - 100033d4
// Signature: undefined FUN_1000338d(LPVOID param_1)


void __cdecl FUN_1000338d(LPVOID param_1)

{
  uint *puVar1;
  
  if (param_1 != (LPVOID)0x0) {
    FUN_1000328a(9);
    puVar1 = (uint *)FUN_10003cd3((int)param_1);
    if (puVar1 != (uint *)0x0) {
      FUN_10003cfe(puVar1,(uint)param_1);
      FUN_100032eb(9);
      return;
    }
    FUN_100032eb(9);
    HeapFree(DAT_100092e4,0,param_1);
  }
  return;
}


