// Program: MSDriver.dll
// Function: FUN_10004b86
// Entry: 10004b86
// Body: 10004b86 - 10004bb4
// Signature: undefined FUN_10004b86(uint param_1)


void __cdecl FUN_10004b86(uint param_1)

{
  if ((param_1 < 0x100092e0) || (0x10009540 < param_1)) {
    EnterCriticalSection((LPCRITICAL_SECTION)(param_1 + 0x20));
    return;
  }
  FUN_1000277c(((int)(param_1 + 0xefff6d20) >> 5) + 0x1c);
  return;
}


