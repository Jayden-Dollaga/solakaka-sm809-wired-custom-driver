// Program: Hook.dll
// Function: FUN_10002f9e
// Entry: 10002f9e
// Body: 10002f9e - 10002fc0
// Signature: undefined FUN_10002f9e(int param_1, int param_2)


void __cdecl FUN_10002f9e(int param_1,int param_2)

{
  if (param_1 < 0x14) {
    FUN_100032eb(param_1 + 0x1c);
    return;
  }
  LeaveCriticalSection((LPCRITICAL_SECTION)(param_2 + 0x20));
  return;
}


