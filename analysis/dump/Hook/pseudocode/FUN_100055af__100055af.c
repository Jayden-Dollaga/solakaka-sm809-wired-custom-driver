// Program: Hook.dll
// Function: FUN_100055af
// Entry: 100055af
// Body: 100055af - 1000560b
// Signature: undefined4 FUN_100055af(uint param_1)


undefined4 __cdecl FUN_100055af(uint param_1)

{
  undefined4 uVar1;
  DWORD *pDVar2;
  
  if ((param_1 < DAT_10009400) &&
     ((*(byte *)((&DAT_10009300)[(int)param_1 >> 5] + 4 + (param_1 & 0x1f) * 0x24) & 1) != 0)) {
    FUN_100047b4(param_1);
    uVar1 = FUN_1000560c(param_1);
    FUN_10004813(param_1);
    return uVar1;
  }
  pDVar2 = FUN_100046e1();
  *pDVar2 = 9;
  pDVar2 = FUN_100046ea();
  *pDVar2 = 0;
  return 0xffffffff;
}


