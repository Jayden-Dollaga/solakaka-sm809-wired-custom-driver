// Program: MSDriver.dll
// Function: FUN_10004c07
// Entry: 10004c07
// Body: 10004c07 - 10004c29
// Signature: undefined FUN_10004c07(int param_1, int param_2)


void __cdecl FUN_10004c07(int param_1,int param_2)

{
  if (param_1 < 0x14) {
    FUN_100027dd(param_1 + 0x1c);
    return;
  }
  LeaveCriticalSection((LPCRITICAL_SECTION)(param_2 + 0x20));
  return;
}


