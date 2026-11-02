// Program: MSDriver.dll
// Function: FUN_10004d04
// Entry: 10004d04
// Body: 10004d04 - 10004d6c
// Signature: int FUN_10004d04(LPSTR param_1, WCHAR param_2)


int __cdecl FUN_10004d04(LPSTR param_1,WCHAR param_2)

{
  LPSTR lpMultiByteStr;
  int iVar1;
  DWORD *pDVar2;
  
  lpMultiByteStr = param_1;
  if (param_1 == (LPSTR)0x0) {
    return 0;
  }
  if (DAT_1000a0f0 == 0) {
    if ((ushort)param_2 < 0x100) {
      *param_1 = (CHAR)param_2;
      return 1;
    }
  }
  else {
    param_1 = (LPSTR)0x0;
    iVar1 = WideCharToMultiByte(DAT_1000a100,0x220,&param_2,1,lpMultiByteStr,DAT_10009b94,
                                (LPCSTR)0x0,(LPBOOL)&param_1);
    if ((iVar1 != 0) && (param_1 == (LPSTR)0x0)) {
      return iVar1;
    }
  }
  pDVar2 = FUN_10005881();
  *pDVar2 = 0x2a;
  return -1;
}


