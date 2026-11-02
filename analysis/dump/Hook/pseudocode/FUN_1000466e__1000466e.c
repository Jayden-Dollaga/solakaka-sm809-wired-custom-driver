// Program: Hook.dll
// Function: FUN_1000466e
// Entry: 1000466e
// Body: 1000466e - 100046e0
// Signature: undefined FUN_1000466e(uint param_1)


void __cdecl FUN_1000466e(uint param_1)

{
  DWORD *pDVar1;
  uint *puVar2;
  int iVar3;
  
  pDVar1 = FUN_100046ea();
  iVar3 = 0;
  *pDVar1 = param_1;
  puVar2 = &DAT_10007850;
  do {
    if (param_1 == *puVar2) {
      pDVar1 = FUN_100046e1();
      *pDVar1 = *(DWORD *)(iVar3 * 8 + 0x10007854);
      return;
    }
    puVar2 = puVar2 + 2;
    iVar3 = iVar3 + 1;
  } while ((int)puVar2 < 0x100079b8);
  if ((0x12 < param_1) && (param_1 < 0x25)) {
    pDVar1 = FUN_100046e1();
    *pDVar1 = 0xd;
    return;
  }
  if ((param_1 < 0xbc) || (0xca < param_1)) {
    pDVar1 = FUN_100046e1();
    *pDVar1 = 0x16;
    return;
  }
  pDVar1 = FUN_100046e1();
  *pDVar1 = 8;
  return;
}


