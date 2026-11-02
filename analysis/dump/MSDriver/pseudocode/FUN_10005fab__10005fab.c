// Program: MSDriver.dll
// Function: FUN_10005fab
// Entry: 10005fab
// Body: 10005fab - 1000603d
// Signature: undefined4 FUN_10005fab(uint param_1)


undefined4 __cdecl FUN_10005fab(uint param_1)

{
  HANDLE hFile;
  BOOL BVar1;
  DWORD DVar2;
  DWORD *pDVar3;
  int iVar4;
  undefined4 uVar5;
  
  if (DAT_1000b5c0 <= param_1) {
LAB_1000602c:
    pDVar3 = FUN_10005881();
    *pDVar3 = 9;
    return 0xffffffff;
  }
  iVar4 = (param_1 & 0x1f) * 0x24;
  if ((*(byte *)((&DAT_1000b4c0)[(int)param_1 >> 5] + 4 + iVar4) & 1) == 0) goto LAB_1000602c;
  FUN_10005954(param_1);
  if ((*(byte *)((&DAT_1000b4c0)[(int)param_1 >> 5] + 4 + iVar4) & 1) != 0) {
    hFile = (HANDLE)FUN_10005912(param_1);
    BVar1 = FlushFileBuffers(hFile);
    if (BVar1 == 0) {
      DVar2 = GetLastError();
    }
    else {
      DVar2 = 0;
    }
    uVar5 = 0;
    if (DVar2 == 0) goto LAB_10006021;
    pDVar3 = FUN_1000588a();
    *pDVar3 = DVar2;
  }
  pDVar3 = FUN_10005881();
  *pDVar3 = 9;
  uVar5 = 0xffffffff;
LAB_10006021:
  FUN_100059b3(param_1);
  return uVar5;
}


