// Program: SM809 mouse Software.exe
// Function: FUN_00420a35
// Entry: 00420a35
// Body: 00420a35 - 00420a77
// Signature: uint FUN_00420a35(void)


uint FUN_00420a35(void)

{
  HMODULE pHVar1;
  int *piVar2;
  
  pHVar1 = GetModuleHandleW((LPCWSTR)0x0);
  if ((((pHVar1 == (HMODULE)0x0) || ((short)pHVar1->unused != 0x5a4d)) ||
      (piVar2 = (int *)((int)&pHVar1->unused + pHVar1[0xf].unused), *piVar2 != 0x4550)) ||
     (((pHVar1 = (HMODULE)0x10b, (short)piVar2[6] != 0x10b || ((uint)piVar2[0x1d] < 0xf)) ||
      (piVar2[0x3a] == 0)))) {
    return (uint)pHVar1 & 0xffffff00;
  }
  return 0x101;
}


