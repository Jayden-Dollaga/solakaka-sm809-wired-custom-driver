// Program: Hook.dll
// Function: FUN_100051c2
// Entry: 100051c2
// Body: 100051c2 - 10005254
// Signature: undefined4 FUN_100051c2(uint param_1)


undefined4 __cdecl FUN_100051c2(uint param_1)

{
  HANDLE hFile;
  BOOL BVar1;
  DWORD DVar2;
  DWORD *pDVar3;
  int iVar4;
  undefined4 uVar5;
  
  if (DAT_10009400 <= param_1) {
LAB_10005243:
    pDVar3 = FUN_100046e1();
    *pDVar3 = 9;
    return 0xffffffff;
  }
  iVar4 = (param_1 & 0x1f) * 0x24;
  if ((*(byte *)((&DAT_10009300)[(int)param_1 >> 5] + 4 + iVar4) & 1) == 0) goto LAB_10005243;
  FUN_100047b4(param_1);
  if ((*(byte *)((&DAT_10009300)[(int)param_1 >> 5] + 4 + iVar4) & 1) != 0) {
    hFile = (HANDLE)FUN_10004772(param_1);
    BVar1 = FlushFileBuffers(hFile);
    if (BVar1 == 0) {
      DVar2 = GetLastError();
    }
    else {
      DVar2 = 0;
    }
    uVar5 = 0;
    if (DVar2 == 0) goto LAB_10005238;
    pDVar3 = FUN_100046ea();
    *pDVar3 = DVar2;
  }
  pDVar3 = FUN_100046e1();
  *pDVar3 = 9;
  uVar5 = 0xffffffff;
LAB_10005238:
  FUN_10004813(param_1);
  return uVar5;
}


