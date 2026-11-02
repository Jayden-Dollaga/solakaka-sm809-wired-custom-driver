// Program: Hook.dll
// Function: FUN_100044de
// Entry: 100044de
// Body: 100044de - 10004566
// Signature: int FUN_100044de(undefined4 param_1, undefined4 param_2, undefined4 param_3)


int __cdecl FUN_100044de(undefined4 param_1,undefined4 param_2,undefined4 param_3)

{
  HMODULE hModule;
  int iVar1;
  
  iVar1 = 0;
  if (DAT_10007efc == (FARPROC)0x0) {
    hModule = LoadLibraryA("user32.dll");
    if (hModule != (HMODULE)0x0) {
      DAT_10007efc = GetProcAddress(hModule,"MessageBoxA");
      if (DAT_10007efc != (FARPROC)0x0) {
        DAT_10007f00 = GetProcAddress(hModule,"GetActiveWindow");
        DAT_10007f04 = GetProcAddress(hModule,"GetLastActivePopup");
        goto LAB_1000452d;
      }
    }
    iVar1 = 0;
  }
  else {
LAB_1000452d:
    if (DAT_10007f00 != (FARPROC)0x0) {
      iVar1 = (*DAT_10007f00)();
      if ((iVar1 != 0) && (DAT_10007f04 != (FARPROC)0x0)) {
        iVar1 = (*DAT_10007f04)(iVar1);
      }
    }
    iVar1 = (*DAT_10007efc)(iVar1,param_1,param_2,param_3);
  }
  return iVar1;
}


