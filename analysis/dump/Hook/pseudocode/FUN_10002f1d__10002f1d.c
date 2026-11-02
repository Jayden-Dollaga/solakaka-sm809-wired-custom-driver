// Program: Hook.dll
// Function: FUN_10002f1d
// Entry: 10002f1d
// Body: 10002f1d - 10002f4b
// Signature: undefined FUN_10002f1d(uint param_1)


void __cdecl FUN_10002f1d(uint param_1)

{
  if ((param_1 < 0x10007140) || (0x100073a0 < param_1)) {
    EnterCriticalSection((LPCRITICAL_SECTION)(param_1 + 0x20));
    return;
  }
  FUN_1000328a(((int)(param_1 + 0xefff8ec0) >> 5) + 0x1c);
  return;
}


