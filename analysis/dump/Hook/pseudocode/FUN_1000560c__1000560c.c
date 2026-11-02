// Program: Hook.dll
// Function: FUN_1000560c
// Entry: 1000560c
// Body: 1000560c - 1000568e
// Signature: undefined4 FUN_1000560c(uint param_1)


undefined4 __cdecl FUN_1000560c(uint param_1)

{
  int iVar1;
  int iVar2;
  HANDLE hObject;
  BOOL BVar3;
  DWORD DVar4;
  undefined4 uVar5;
  
  iVar1 = FUN_10004772(param_1);
  if (iVar1 != -1) {
    if ((param_1 == 1) || (param_1 == 2)) {
      iVar1 = FUN_10004772(2);
      iVar2 = FUN_10004772(1);
      if (iVar2 == iVar1) goto LAB_1000565a;
    }
    hObject = (HANDLE)FUN_10004772(param_1);
    BVar3 = CloseHandle(hObject);
    if (BVar3 == 0) {
      DVar4 = GetLastError();
      goto LAB_1000565c;
    }
  }
LAB_1000565a:
  DVar4 = 0;
LAB_1000565c:
  FUN_100046f3(param_1);
  *(undefined1 *)((&DAT_10009300)[(int)param_1 >> 5] + 4 + (param_1 & 0x1f) * 0x24) = 0;
  if (DVar4 == 0) {
    uVar5 = 0;
  }
  else {
    FUN_1000466e(DVar4);
    uVar5 = 0xffffffff;
  }
  return uVar5;
}


