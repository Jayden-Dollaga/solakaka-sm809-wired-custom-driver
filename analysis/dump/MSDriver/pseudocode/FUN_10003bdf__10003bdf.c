// Program: MSDriver.dll
// Function: FUN_10003bdf
// Entry: 10003bdf
// Body: 10003bdf - 10003c7e
// Signature: undefined FUN_10003bdf(LPVOID param_1)


void __cdecl FUN_10003bdf(LPVOID param_1)

{
  if (DAT_10009218 == 0xffffffff) {
    return;
  }
  if ((param_1 != (LPVOID)0x0) || (param_1 = TlsGetValue(DAT_10009218), param_1 != (LPVOID)0x0)) {
    if (*(LPVOID *)((int)param_1 + 0x24) != (LPVOID)0x0) {
      FUN_100022da(*(LPVOID *)((int)param_1 + 0x24));
    }
    if (*(LPVOID *)((int)param_1 + 0x28) != (LPVOID)0x0) {
      FUN_100022da(*(LPVOID *)((int)param_1 + 0x28));
    }
    if (*(LPVOID *)((int)param_1 + 0x30) != (LPVOID)0x0) {
      FUN_100022da(*(LPVOID *)((int)param_1 + 0x30));
    }
    if (*(LPVOID *)((int)param_1 + 0x38) != (LPVOID)0x0) {
      FUN_100022da(*(LPVOID *)((int)param_1 + 0x38));
    }
    if (*(LPVOID *)((int)param_1 + 0x40) != (LPVOID)0x0) {
      FUN_100022da(*(LPVOID *)((int)param_1 + 0x40));
    }
    if (*(LPVOID *)((int)param_1 + 0x44) != (LPVOID)0x0) {
      FUN_100022da(*(LPVOID *)((int)param_1 + 0x44));
    }
    if (*(undefined **)((int)param_1 + 0x50) != &DAT_10009790) {
      FUN_100022da(*(undefined **)((int)param_1 + 0x50));
    }
    FUN_100022da(param_1);
  }
  TlsSetValue(DAT_10009218,(LPVOID)0x0);
  return;
}


