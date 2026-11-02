// Program: MSDriver.dll
// Function: FUN_10004bb5
// Entry: 10004bb5
// Body: 10004bb5 - 10004bd7
// Signature: undefined FUN_10004bb5(int param_1, int param_2)


void __cdecl FUN_10004bb5(int param_1,int param_2)

{
  if (param_1 < 0x14) {
    FUN_1000277c(param_1 + 0x1c);
    return;
  }
  EnterCriticalSection((LPCRITICAL_SECTION)(param_2 + 0x20));
  return;
}


