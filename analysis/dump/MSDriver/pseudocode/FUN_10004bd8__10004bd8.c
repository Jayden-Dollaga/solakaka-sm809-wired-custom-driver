// Program: MSDriver.dll
// Function: FUN_10004bd8
// Entry: 10004bd8
// Body: 10004bd8 - 10004c06
// Signature: undefined FUN_10004bd8(uint param_1)


void __cdecl FUN_10004bd8(uint param_1)

{
  if ((param_1 < 0x100092e0) || (0x10009540 < param_1)) {
    LeaveCriticalSection((LPCRITICAL_SECTION)(param_1 + 0x20));
    return;
  }
  FUN_100027dd(((int)(param_1 + 0xefff6d20) >> 5) + 0x1c);
  return;
}


