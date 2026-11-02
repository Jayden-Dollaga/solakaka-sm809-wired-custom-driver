// Program: MSDriver.dll
// Function: FUN_10005685
// Entry: 10005685
// Body: 10005685 - 1000570d
// Signature: int FUN_10005685(undefined4 param_1, undefined4 param_2, undefined4 param_3)


int __cdecl FUN_10005685(undefined4 param_1,undefined4 param_2,undefined4 param_3)

{
  HMODULE hModule;
  int iVar1;
  
  iVar1 = 0;
  if (DAT_1000a0d0 == (FARPROC)0x0) {
    hModule = LoadLibraryA("user32.dll");
    if (hModule != (HMODULE)0x0) {
      DAT_1000a0d0 = GetProcAddress(hModule,"MessageBoxA");
      if (DAT_1000a0d0 != (FARPROC)0x0) {
        DAT_1000a0d4 = GetProcAddress(hModule,"GetActiveWindow");
        DAT_1000a0d8 = GetProcAddress(hModule,"GetLastActivePopup");
        goto LAB_100056d4;
      }
    }
    iVar1 = 0;
  }
  else {
LAB_100056d4:
    if (DAT_1000a0d4 != (FARPROC)0x0) {
      iVar1 = (*DAT_1000a0d4)();
      if ((iVar1 != 0) && (DAT_1000a0d8 != (FARPROC)0x0)) {
        iVar1 = (*DAT_1000a0d8)(iVar1);
      }
    }
    iVar1 = (*DAT_1000a0d0)(iVar1,param_1,param_2,param_3);
  }
  return iVar1;
}


