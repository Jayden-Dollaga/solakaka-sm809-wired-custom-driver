// Program: Hook.dll
// Function: FUN_10002f4c
// Entry: 10002f4c
// Body: 10002f4c - 10002f6e
// Signature: undefined FUN_10002f4c(int param_1, int param_2)


void __cdecl FUN_10002f4c(int param_1,int param_2)

{
  if (param_1 < 0x14) {
    FUN_1000328a(param_1 + 0x1c);
    return;
  }
  EnterCriticalSection((LPCRITICAL_SECTION)(param_2 + 0x20));
  return;
}


