// Program: Hook.dll
// Function: FUN_10002207
// Entry: 10002207
// Body: 10002207 - 100022a6
// Signature: undefined FUN_10002207(LPVOID param_1)


void __cdecl FUN_10002207(LPVOID param_1)

{
  if (DAT_10007080 == 0xffffffff) {
    return;
  }
  if ((param_1 != (LPVOID)0x0) || (param_1 = TlsGetValue(DAT_10007080), param_1 != (LPVOID)0x0)) {
    if (*(LPVOID *)((int)param_1 + 0x24) != (LPVOID)0x0) {
      FUN_1000338d(*(LPVOID *)((int)param_1 + 0x24));
    }
    if (*(LPVOID *)((int)param_1 + 0x28) != (LPVOID)0x0) {
      FUN_1000338d(*(LPVOID *)((int)param_1 + 0x28));
    }
    if (*(LPVOID *)((int)param_1 + 0x30) != (LPVOID)0x0) {
      FUN_1000338d(*(LPVOID *)((int)param_1 + 0x30));
    }
    if (*(LPVOID *)((int)param_1 + 0x38) != (LPVOID)0x0) {
      FUN_1000338d(*(LPVOID *)((int)param_1 + 0x38));
    }
    if (*(LPVOID *)((int)param_1 + 0x40) != (LPVOID)0x0) {
      FUN_1000338d(*(LPVOID *)((int)param_1 + 0x40));
    }
    if (*(LPVOID *)((int)param_1 + 0x44) != (LPVOID)0x0) {
      FUN_1000338d(*(LPVOID *)((int)param_1 + 0x44));
    }
    if (*(undefined **)((int)param_1 + 0x50) != &DAT_100076b0) {
      FUN_1000338d(*(undefined **)((int)param_1 + 0x50));
    }
    FUN_1000338d(param_1);
  }
  TlsSetValue(DAT_10007080,(LPVOID)0x0);
  return;
}


