// Program: Hook.dll
// Function: FUN_10004772
// Entry: 10004772
// Body: 10004772 - 100047b3
// Signature: undefined4 FUN_10004772(uint param_1)


undefined4 __cdecl FUN_10004772(uint param_1)

{
  DWORD *pDVar1;
  
  if ((param_1 < DAT_10009400) &&
     ((*(byte *)((&DAT_10009300)[(int)param_1 >> 5] + 4 + (param_1 & 0x1f) * 0x24) & 1) != 0)) {
    return *(undefined4 *)((&DAT_10009300)[(int)param_1 >> 5] + (param_1 & 0x1f) * 0x24);
  }
  pDVar1 = FUN_100046e1();
  *pDVar1 = 9;
  pDVar1 = FUN_100046ea();
  *pDVar1 = 0;
  return 0xffffffff;
}


