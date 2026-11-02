// Program: Hook.dll
// Function: FUN_100046f3
// Entry: 100046f3
// Body: 100046f3 - 10004771
// Signature: undefined4 FUN_100046f3(uint param_1)


undefined4 __cdecl FUN_100046f3(uint param_1)

{
  int *piVar1;
  DWORD *pDVar2;
  int iVar3;
  DWORD nStdHandle;
  
  if (param_1 < DAT_10009400) {
    iVar3 = (param_1 & 0x1f) * 0x24;
    piVar1 = (int *)((&DAT_10009300)[(int)param_1 >> 5] + iVar3);
    if (((*(byte *)(piVar1 + 1) & 1) != 0) && (*piVar1 != -1)) {
      if (DAT_10007d40 == 1) {
        if (param_1 == 0) {
          nStdHandle = 0xfffffff6;
        }
        else if (param_1 == 1) {
          nStdHandle = 0xfffffff5;
        }
        else {
          if (param_1 != 2) goto LAB_1000474f;
          nStdHandle = 0xfffffff4;
        }
        SetStdHandle(nStdHandle,(HANDLE)0x0);
      }
LAB_1000474f:
      *(undefined4 *)((&DAT_10009300)[(int)param_1 >> 5] + iVar3) = 0xffffffff;
      return 0;
    }
  }
  pDVar2 = FUN_100046e1();
  *pDVar2 = 9;
  pDVar2 = FUN_100046ea();
  *pDVar2 = 0;
  return 0xffffffff;
}


