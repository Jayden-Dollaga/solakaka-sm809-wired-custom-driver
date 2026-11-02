// Program: MSDriver.dll
// Function: FUN_100063ec
// Entry: 100063ec
// Body: 100063ec - 1000646e
// Signature: undefined4 FUN_100063ec(uint param_1)


undefined4 __cdecl FUN_100063ec(uint param_1)

{
  int iVar1;
  int iVar2;
  HANDLE hObject;
  BOOL BVar3;
  DWORD DVar4;
  undefined4 uVar5;
  
  iVar1 = FUN_10005912(param_1);
  if (iVar1 != -1) {
    if ((param_1 == 1) || (param_1 == 2)) {
      iVar1 = FUN_10005912(2);
      iVar2 = FUN_10005912(1);
      if (iVar2 == iVar1) goto LAB_1000643a;
    }
    hObject = (HANDLE)FUN_10005912(param_1);
    BVar3 = CloseHandle(hObject);
    if (BVar3 == 0) {
      DVar4 = GetLastError();
      goto LAB_1000643c;
    }
  }
LAB_1000643a:
  DVar4 = 0;
LAB_1000643c:
  FUN_10005893(param_1);
  *(undefined1 *)((&DAT_1000b4c0)[(int)param_1 >> 5] + 4 + (param_1 & 0x1f) * 0x24) = 0;
  if (DVar4 == 0) {
    uVar5 = 0;
  }
  else {
    FUN_1000580e(DVar4);
    uVar5 = 0xffffffff;
  }
  return uVar5;
}


