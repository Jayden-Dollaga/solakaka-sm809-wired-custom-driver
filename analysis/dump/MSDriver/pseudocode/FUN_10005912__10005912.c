// Program: MSDriver.dll
// Function: FUN_10005912
// Entry: 10005912
// Body: 10005912 - 10005953
// Signature: undefined4 FUN_10005912(uint param_1)


undefined4 __cdecl FUN_10005912(uint param_1)

{
  DWORD *pDVar1;
  
  if ((param_1 < DAT_1000b5c0) &&
     ((*(byte *)((&DAT_1000b4c0)[(int)param_1 >> 5] + 4 + (param_1 & 0x1f) * 0x24) & 1) != 0)) {
    return *(undefined4 *)((&DAT_1000b4c0)[(int)param_1 >> 5] + (param_1 & 0x1f) * 0x24);
  }
  pDVar1 = FUN_10005881();
  *pDVar1 = 9;
  pDVar1 = FUN_1000588a();
  *pDVar1 = 0;
  return 0xffffffff;
}


