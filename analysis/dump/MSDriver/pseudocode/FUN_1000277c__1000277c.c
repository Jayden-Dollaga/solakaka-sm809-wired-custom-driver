// Program: MSDriver.dll
// Function: FUN_1000277c
// Entry: 1000277c
// Body: 1000277c - 100027dc
// Signature: undefined FUN_1000277c(int param_1)


void __cdecl FUN_1000277c(int param_1)

{
  int *piVar1;
  LPCRITICAL_SECTION lpCriticalSection;
  
  piVar1 = &DAT_1000914c + param_1;
  if ((&DAT_1000914c)[param_1] == 0) {
    lpCriticalSection = _malloc(0x18);
    if (lpCriticalSection == (LPCRITICAL_SECTION)0x0) {
      __amsg_exit(0x11);
    }
    FUN_1000277c(0x11);
    if (*piVar1 == 0) {
      InitializeCriticalSection(lpCriticalSection);
      *piVar1 = (int)lpCriticalSection;
    }
    else {
      FUN_100022da(lpCriticalSection);
    }
    FUN_100027dd(0x11);
  }
  EnterCriticalSection((LPCRITICAL_SECTION)*piVar1);
  return;
}


