// Program: Hook.dll
// Function: FUN_1000328a
// Entry: 1000328a
// Body: 1000328a - 100032ea
// Signature: undefined FUN_1000328a(int param_1)


void __cdecl FUN_1000328a(int param_1)

{
  int *piVar1;
  LPCRITICAL_SECTION lpCriticalSection;
  
  piVar1 = &DAT_100075f0 + param_1;
  if ((&DAT_100075f0)[param_1] == 0) {
    lpCriticalSection = _malloc(0x18);
    if (lpCriticalSection == (LPCRITICAL_SECTION)0x0) {
      __amsg_exit(0x11);
    }
    FUN_1000328a(0x11);
    if (*piVar1 == 0) {
      InitializeCriticalSection(lpCriticalSection);
      *piVar1 = (int)lpCriticalSection;
    }
    else {
      FUN_1000338d(lpCriticalSection);
    }
    FUN_100032eb(0x11);
  }
  EnterCriticalSection((LPCRITICAL_SECTION)*piVar1);
  return;
}


