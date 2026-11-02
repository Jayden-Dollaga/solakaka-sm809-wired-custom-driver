// Program: MSDriver.dll
// Function: FUN_100047fa
// Entry: 100047fa
// Body: 100047fa - 1000486c
// Signature: DWORD FUN_100047fa(uint param_1, LONG param_2, DWORD param_3)


DWORD __cdecl FUN_100047fa(uint param_1,LONG param_2,DWORD param_3)

{
  byte *pbVar1;
  HANDLE hFile;
  DWORD *pDVar2;
  DWORD DVar3;
  uint uVar4;
  
  hFile = (HANDLE)FUN_10005912(param_1);
  if (hFile == (HANDLE)0xffffffff) {
    pDVar2 = FUN_10005881();
    *pDVar2 = 9;
  }
  else {
    DVar3 = SetFilePointer(hFile,param_2,(PLONG)0x0,param_3);
    if (DVar3 == 0xffffffff) {
      uVar4 = GetLastError();
    }
    else {
      uVar4 = 0;
    }
    if (uVar4 == 0) {
      pbVar1 = (byte *)((&DAT_1000b4c0)[(int)param_1 >> 5] + 4 + (param_1 & 0x1f) * 0x24);
      *pbVar1 = *pbVar1 & 0xfd;
      return DVar3;
    }
    FUN_1000580e(uVar4);
  }
  return 0xffffffff;
}


