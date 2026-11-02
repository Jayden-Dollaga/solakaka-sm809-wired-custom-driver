// Program: MSDriver.dll
// Function: FUN_10005954
// Entry: 10005954
// Body: 10005954 - 100059b2
// Signature: undefined FUN_10005954(uint param_1)


void __cdecl FUN_10005954(uint param_1)

{
  int iVar1;
  int iVar2;
  
  iVar2 = (param_1 & 0x1f) * 0x24;
  iVar1 = (&DAT_1000b4c0)[(int)param_1 >> 5] + iVar2;
  if (*(int *)(iVar1 + 8) == 0) {
    FUN_1000277c(0x11);
    if (*(int *)(iVar1 + 8) == 0) {
      InitializeCriticalSection((LPCRITICAL_SECTION)(iVar1 + 0xc));
      *(int *)(iVar1 + 8) = *(int *)(iVar1 + 8) + 1;
    }
    FUN_100027dd(0x11);
  }
  EnterCriticalSection((LPCRITICAL_SECTION)((&DAT_1000b4c0)[(int)param_1 >> 5] + 0xc + iVar2));
  return;
}


