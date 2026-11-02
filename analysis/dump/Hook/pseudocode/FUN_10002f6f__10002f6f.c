// Program: Hook.dll
// Function: FUN_10002f6f
// Entry: 10002f6f
// Body: 10002f6f - 10002f9d
// Signature: undefined FUN_10002f6f(uint param_1)


void __cdecl FUN_10002f6f(uint param_1)

{
  if ((param_1 < 0x10007140) || (0x100073a0 < param_1)) {
    LeaveCriticalSection((LPCRITICAL_SECTION)(param_1 + 0x20));
    return;
  }
  FUN_100032eb(((int)(param_1 + 0xefff8ec0) >> 5) + 0x1c);
  return;
}


