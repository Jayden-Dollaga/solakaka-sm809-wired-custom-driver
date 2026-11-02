// Program: MSDriver.dll
// Function: FUN_10005893
// Entry: 10005893
// Body: 10005893 - 10005911
// Signature: undefined4 FUN_10005893(uint param_1)


undefined4 __cdecl FUN_10005893(uint param_1)

{
  int *piVar1;
  DWORD *pDVar2;
  int iVar3;
  DWORD nStdHandle;
  
  if (param_1 < DAT_1000b5c0) {
    iVar3 = (param_1 & 0x1f) * 0x24;
    piVar1 = (int *)((&DAT_1000b4c0)[(int)param_1 >> 5] + iVar3);
    if (((*(byte *)(piVar1 + 1) & 1) != 0) && (*piVar1 != -1)) {
      if (DAT_10009f0c == 1) {
        if (param_1 == 0) {
          nStdHandle = 0xfffffff6;
        }
        else if (param_1 == 1) {
          nStdHandle = 0xfffffff5;
        }
        else {
          if (param_1 != 2) goto LAB_100058ef;
          nStdHandle = 0xfffffff4;
        }
        SetStdHandle(nStdHandle,(HANDLE)0x0);
      }
LAB_100058ef:
      *(undefined4 *)((&DAT_1000b4c0)[(int)param_1 >> 5] + iVar3) = 0xffffffff;
      return 0;
    }
  }
  pDVar2 = FUN_10005881();
  *pDVar2 = 9;
  pDVar2 = FUN_1000588a();
  *pDVar2 = 0;
  return 0xffffffff;
}


