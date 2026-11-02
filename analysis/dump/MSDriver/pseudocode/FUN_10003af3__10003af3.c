// Program: MSDriver.dll
// Function: FUN_10003af3
// Entry: 10003af3
// Body: 10003af3 - 10003b46
// Signature: undefined4 FUN_10003af3(void)


undefined4 FUN_10003af3(void)

{
  DWORD *lpTlsValue;
  BOOL BVar1;
  DWORD DVar2;
  
  FUN_100026e7();
  DAT_10009218 = TlsAlloc();
  if (DAT_10009218 != 0xffffffff) {
    lpTlsValue = (DWORD *)FUN_10002322(1,0x74);
    if (lpTlsValue != (DWORD *)0x0) {
      BVar1 = TlsSetValue(DAT_10009218,lpTlsValue);
      if (BVar1 != 0) {
        FUN_10003b65((int)lpTlsValue);
        DVar2 = GetCurrentThreadId();
        lpTlsValue[1] = 0xffffffff;
        *lpTlsValue = DVar2;
        return 1;
      }
    }
  }
  return 0;
}


