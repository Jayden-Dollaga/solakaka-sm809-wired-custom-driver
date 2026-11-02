// Program: MSDriver.dll
// Function: FUN_10005de5
// Entry: 10005de5
// Body: 10005de5 - 10005f2d
// Signature: BOOL FUN_10005de5(DWORD param_1, LPCSTR param_2, int param_3, LPWORD param_4, UINT param_5, LCID param_6, int param_7)


BOOL __cdecl
FUN_10005de5(DWORD param_1,LPCSTR param_2,int param_3,LPWORD param_4,UINT param_5,LCID param_6,
            int param_7)

{
  WCHAR *pWVar1;
  BOOL BVar2;
  int iVar3;
  undefined1 unaff_DI;
  undefined1 uStack00000000;
  WCHAR aWStack_2a [5];
  WORD local_20 [2];
  undefined1 *local_1c;
  void *local_14;
  undefined1 *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_10007528;
  puStack_10 = &LAB_10006284;
  local_14 = ExceptionList;
  local_1c = (undefined1 *)(aWStack_2a + -7);
  ExceptionList = &local_14;
  pWVar1 = aWStack_2a + -7;
  if (DAT_1000a10c == 0) {
    iVar3 = 1;
    ExceptionList = &local_14;
    BVar2 = GetStringTypeW(1,L"",1,local_20);
    if (BVar2 == 0) {
      BVar2 = GetStringTypeA(0,1,"",1,local_20);
      if (BVar2 == 0) {
        ExceptionList = local_14;
        return 0;
      }
      iVar3 = 2;
    }
    DAT_1000a10c = iVar3;
    pWVar1 = (WCHAR *)local_1c;
  }
  local_1c = (undefined1 *)pWVar1;
  if (DAT_1000a10c == 2) {
    if (param_6 == 0) {
      param_6 = DAT_1000a0f0;
    }
    BVar2 = GetStringTypeA(param_6,param_1,param_2,param_3,param_4);
    ExceptionList = local_14;
    return BVar2;
  }
  if (DAT_1000a10c == 1) {
    if (param_5 == 0) {
      param_5 = DAT_1000a100;
    }
    iVar3 = MultiByteToWideChar(param_5,(-(uint)(param_7 != 0) & 8) + 1,param_2,param_3,(LPWSTR)0x0,
                                0);
    if (iVar3 != 0) {
      local_8 = 0;
      FUN_10006360(unaff_DI);
      local_1c = (undefined1 *)(aWStack_2a + -7);
      _memset(aWStack_2a + -7,0,iVar3 * 2);
      local_8 = 0xffffffff;
      if ((&uStack00000000 != (undefined1 *)0x38) &&
         (iVar3 = MultiByteToWideChar(param_5,1,param_2,param_3,aWStack_2a + -7,iVar3), iVar3 != 0))
      {
        BVar2 = GetStringTypeW(param_1,aWStack_2a + -7,iVar3,param_4);
        ExceptionList = local_14;
        return BVar2;
      }
    }
  }
  ExceptionList = local_14;
  return 0;
}


