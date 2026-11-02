// Program: Hook.dll
// Function: FUN_100047b4
// Entry: 100047b4
// Body: 100047b4 - 10004812
// Signature: undefined FUN_100047b4(uint param_1)


void __cdecl FUN_100047b4(uint param_1)

{
  int iVar1;
  int iVar2;
  
  iVar2 = (param_1 & 0x1f) * 0x24;
  iVar1 = (&DAT_10009300)[(int)param_1 >> 5] + iVar2;
  if (*(int *)(iVar1 + 8) == 0) {
    FUN_1000328a(0x11);
    if (*(int *)(iVar1 + 8) == 0) {
      InitializeCriticalSection((LPCRITICAL_SECTION)(iVar1 + 0xc));
      *(int *)(iVar1 + 8) = *(int *)(iVar1 + 8) + 1;
    }
    FUN_100032eb(0x11);
  }
  EnterCriticalSection((LPCRITICAL_SECTION)((&DAT_10009300)[(int)param_1 >> 5] + 0xc + iVar2));
  return;
}


