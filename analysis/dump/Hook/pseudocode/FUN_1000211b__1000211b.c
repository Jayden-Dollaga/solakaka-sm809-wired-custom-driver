// Program: Hook.dll
// Function: FUN_1000211b
// Entry: 1000211b
// Body: 1000211b - 1000216e
// Signature: undefined4 FUN_1000211b(void)


undefined4 FUN_1000211b(void)

{
  DWORD *lpTlsValue;
  BOOL BVar1;
  DWORD DVar2;
  
  FUN_100031f5();
  DAT_10007080 = TlsAlloc();
  if (DAT_10007080 != 0xffffffff) {
    lpTlsValue = (DWORD *)FUN_10003300(1,0x74);
    if (lpTlsValue != (DWORD *)0x0) {
      BVar1 = TlsSetValue(DAT_10007080,lpTlsValue);
      if (BVar1 != 0) {
        FUN_1000218d((int)lpTlsValue);
        DVar2 = GetCurrentThreadId();
        lpTlsValue[1] = 0xffffffff;
        *lpTlsValue = DVar2;
        return 1;
      }
    }
  }
  return 0;
}


