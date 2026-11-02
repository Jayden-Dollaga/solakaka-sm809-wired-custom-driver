// Program: MSDriver.dll
// Function: FUN_10004795
// Entry: 10004795
// Body: 10004795 - 100047f9
// Signature: DWORD FUN_10004795(uint param_1, LONG param_2, DWORD param_3)


DWORD __cdecl FUN_10004795(uint param_1,LONG param_2,DWORD param_3)

{
  DWORD DVar1;
  DWORD *pDVar2;
  
  if ((param_1 < DAT_1000b5c0) &&
     ((*(byte *)((&DAT_1000b4c0)[(int)param_1 >> 5] + 4 + (param_1 & 0x1f) * 0x24) & 1) != 0)) {
    FUN_10005954(param_1);
    DVar1 = FUN_100047fa(param_1,param_2,param_3);
    FUN_100059b3(param_1);
    return DVar1;
  }
  pDVar2 = FUN_10005881();
  *pDVar2 = 9;
  pDVar2 = FUN_1000588a();
  *pDVar2 = 0;
  return 0xffffffff;
}


