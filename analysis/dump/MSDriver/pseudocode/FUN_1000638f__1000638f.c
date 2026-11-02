// Program: MSDriver.dll
// Function: FUN_1000638f
// Entry: 1000638f
// Body: 1000638f - 100063eb
// Signature: undefined4 FUN_1000638f(uint param_1)


undefined4 __cdecl FUN_1000638f(uint param_1)

{
  undefined4 uVar1;
  DWORD *pDVar2;
  
  if ((param_1 < DAT_1000b5c0) &&
     ((*(byte *)((&DAT_1000b4c0)[(int)param_1 >> 5] + 4 + (param_1 & 0x1f) * 0x24) & 1) != 0)) {
    FUN_10005954(param_1);
    uVar1 = FUN_100063ec(param_1);
    FUN_100059b3(param_1);
    return uVar1;
  }
  pDVar2 = FUN_10005881();
  *pDVar2 = 9;
  pDVar2 = FUN_1000588a();
  *pDVar2 = 0;
  return 0xffffffff;
}


