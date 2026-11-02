// Program: MSDriver.dll
// Function: FUN_1000580e
// Entry: 1000580e
// Body: 1000580e - 10005880
// Signature: undefined FUN_1000580e(uint param_1)


void __cdecl FUN_1000580e(uint param_1)

{
  DWORD *pDVar1;
  uint *puVar2;
  int iVar3;
  
  pDVar1 = FUN_1000588a();
  iVar3 = 0;
  *pDVar1 = param_1;
  puVar2 = &DAT_10009920;
  do {
    if (param_1 == *puVar2) {
      pDVar1 = FUN_10005881();
      *pDVar1 = *(DWORD *)(iVar3 * 8 + 0x10009924);
      return;
    }
    puVar2 = puVar2 + 2;
    iVar3 = iVar3 + 1;
  } while ((int)puVar2 < 0x10009a88);
  if ((0x12 < param_1) && (param_1 < 0x25)) {
    pDVar1 = FUN_10005881();
    *pDVar1 = 0xd;
    return;
  }
  if ((param_1 < 0xbc) || (0xca < param_1)) {
    pDVar1 = FUN_10005881();
    *pDVar1 = 0x16;
    return;
  }
  pDVar1 = FUN_10005881();
  *pDVar1 = 8;
  return;
}


