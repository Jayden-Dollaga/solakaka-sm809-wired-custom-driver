// Program: Hook.dll
// Function: FUN_10002c04
// Entry: 10002c04
// Body: 10002c04 - 10002c68
// Signature: int FUN_10002c04(uint param_1, char * param_2, DWORD param_3)


int __cdecl FUN_10002c04(uint param_1,char *param_2,DWORD param_3)

{
  int iVar1;
  DWORD *pDVar2;
  
  if ((param_1 < DAT_10009400) &&
     ((*(byte *)((&DAT_10009300)[(int)param_1 >> 5] + 4 + (param_1 & 0x1f) * 0x24) & 1) != 0)) {
    FUN_100047b4(param_1);
    iVar1 = FUN_10002c69(param_1,param_2,param_3);
    FUN_10004813(param_1);
    return iVar1;
  }
  pDVar2 = FUN_100046e1();
  *pDVar2 = 9;
  pDVar2 = FUN_100046ea();
  *pDVar2 = 0;
  return -1;
}


