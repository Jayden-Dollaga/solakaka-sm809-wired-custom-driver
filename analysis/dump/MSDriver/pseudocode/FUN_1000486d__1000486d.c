// Program: MSDriver.dll
// Function: FUN_1000486d
// Entry: 1000486d
// Body: 1000486d - 100048d1
// Signature: int FUN_1000486d(uint param_1, char * param_2, DWORD param_3)


int __cdecl FUN_1000486d(uint param_1,char *param_2,DWORD param_3)

{
  int iVar1;
  DWORD *pDVar2;
  
  if ((param_1 < DAT_1000b5c0) &&
     ((*(byte *)((&DAT_1000b4c0)[(int)param_1 >> 5] + 4 + (param_1 & 0x1f) * 0x24) & 1) != 0)) {
    FUN_10005954(param_1);
    iVar1 = FUN_100048d2(param_1,param_2,param_3);
    FUN_100059b3(param_1);
    return iVar1;
  }
  pDVar2 = FUN_10005881();
  *pDVar2 = 9;
  pDVar2 = FUN_1000588a();
  *pDVar2 = 0;
  return -1;
}


