// Program: Hook.dll
// Function: FUN_100021a0
// Entry: 100021a0
// Body: 100021a0 - 10002206
// Signature: DWORD * FUN_100021a0(void)


DWORD * FUN_100021a0(void)

{
  DWORD dwErrCode;
  DWORD *lpTlsValue;
  BOOL BVar1;
  DWORD DVar2;
  
  dwErrCode = GetLastError();
  lpTlsValue = TlsGetValue(DAT_10007080);
  if (lpTlsValue == (DWORD *)0x0) {
    lpTlsValue = (DWORD *)FUN_10003300(1,0x74);
    if (lpTlsValue != (DWORD *)0x0) {
      BVar1 = TlsSetValue(DAT_10007080,lpTlsValue);
      if (BVar1 != 0) {
        FUN_1000218d((int)lpTlsValue);
        DVar2 = GetCurrentThreadId();
        lpTlsValue[1] = 0xffffffff;
        *lpTlsValue = DVar2;
        goto LAB_100021fb;
      }
    }
    __amsg_exit(0x10);
  }
LAB_100021fb:
  SetLastError(dwErrCode);
  return lpTlsValue;
}


