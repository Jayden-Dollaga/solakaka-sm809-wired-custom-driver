// Program: MSDriver.dll
// Function: FUN_10003b78
// Entry: 10003b78
// Body: 10003b78 - 10003bde
// Signature: DWORD * FUN_10003b78(void)


DWORD * FUN_10003b78(void)

{
  DWORD dwErrCode;
  DWORD *lpTlsValue;
  BOOL BVar1;
  DWORD DVar2;
  
  dwErrCode = GetLastError();
  lpTlsValue = TlsGetValue(DAT_10009218);
  if (lpTlsValue == (DWORD *)0x0) {
    lpTlsValue = (DWORD *)FUN_10002322(1,0x74);
    if (lpTlsValue != (DWORD *)0x0) {
      BVar1 = TlsSetValue(DAT_10009218,lpTlsValue);
      if (BVar1 != 0) {
        FUN_10003b65((int)lpTlsValue);
        DVar2 = GetCurrentThreadId();
        lpTlsValue[1] = 0xffffffff;
        *lpTlsValue = DVar2;
        goto LAB_10003bd3;
      }
    }
    __amsg_exit(0x10);
  }
LAB_10003bd3:
  SetLastError(dwErrCode);
  return lpTlsValue;
}


