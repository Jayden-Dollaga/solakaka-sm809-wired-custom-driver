// Program: Hook.dll
// Function: FUN_10002b2c
// Entry: 10002b2c
// Body: 10002b2c - 10002b90
// Signature: DWORD FUN_10002b2c(uint param_1, LONG param_2, DWORD param_3)


DWORD __cdecl FUN_10002b2c(uint param_1,LONG param_2,DWORD param_3)

{
  DWORD DVar1;
  DWORD *pDVar2;
  
  if ((param_1 < DAT_10009400) &&
     ((*(byte *)((&DAT_10009300)[(int)param_1 >> 5] + 4 + (param_1 & 0x1f) * 0x24) & 1) != 0)) {
    FUN_100047b4(param_1);
    DVar1 = FUN_10002b91(param_1,param_2,param_3);
    FUN_10004813(param_1);
    return DVar1;
  }
  pDVar2 = FUN_100046e1();
  *pDVar2 = 9;
  pDVar2 = FUN_100046ea();
  *pDVar2 = 0;
  return 0xffffffff;
}


