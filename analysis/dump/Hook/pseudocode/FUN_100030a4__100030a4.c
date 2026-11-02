// Program: Hook.dll
// Function: FUN_100030a4
// Entry: 100030a4
// Body: 100030a4 - 1000310c
// Signature: int FUN_100030a4(LPSTR param_1, WCHAR param_2)


int __cdecl FUN_100030a4(LPSTR param_1,WCHAR param_2)

{
  LPSTR lpMultiByteStr;
  int iVar1;
  DWORD *pDVar2;
  
  lpMultiByteStr = param_1;
  if (param_1 == (LPSTR)0x0) {
    return 0;
  }
  if (DAT_10007f1c == 0) {
    if ((ushort)param_2 < 0x100) {
      *param_1 = (CHAR)param_2;
      return 1;
    }
  }
  else {
    param_1 = (LPSTR)0x0;
    iVar1 = WideCharToMultiByte(DAT_10007f2c,0x220,&param_2,1,lpMultiByteStr,DAT_10007ac4,
                                (LPCSTR)0x0,(LPBOOL)&param_1);
    if ((iVar1 != 0) && (param_1 == (LPSTR)0x0)) {
      return iVar1;
    }
  }
  pDVar2 = FUN_100046e1();
  *pDVar2 = 0x2a;
  return -1;
}


