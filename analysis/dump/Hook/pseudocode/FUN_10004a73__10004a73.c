// Program: Hook.dll
// Function: FUN_10004a73
// Entry: 10004a73
// Body: 10004a73 - 10004c96
// Signature: int FUN_10004a73(LCID param_1, DWORD param_2, char * param_3, int param_4, LPWSTR param_5, int param_6, UINT param_7, int param_8)


int __cdecl
FUN_10004a73(LCID param_1,DWORD param_2,char *param_3,int param_4,LPWSTR param_5,int param_6,
            UINT param_7,int param_8)

{
  int iVar1;
  int iVar2;
  undefined1 unaff_DI;
  undefined1 uStack00000000;
  WCHAR aWStack_2e [13];
  void *local_14;
  undefined1 *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_100064a0;
  puStack_10 = &LAB_100054a4;
  local_14 = ExceptionList;
  ExceptionList = &local_14;
  if (DAT_10007f3c == 0) {
    ExceptionList = &local_14;
    iVar1 = LCMapStringW(0,0x100,L"",1,(LPWSTR)0x0,0);
    if (iVar1 == 0) {
      iVar1 = LCMapStringA(0,0x100,"",1,(LPSTR)0x0,0);
      if (iVar1 == 0) {
        ExceptionList = local_14;
        return 0;
      }
      DAT_10007f3c = 2;
    }
    else {
      DAT_10007f3c = 1;
    }
  }
  if (0 < param_4) {
    param_4 = FUN_10004c97(param_3,param_4);
  }
  if (DAT_10007f3c == 2) {
    iVar1 = LCMapStringA(param_1,param_2,param_3,param_4,(LPSTR)param_5,param_6);
    ExceptionList = local_14;
    return iVar1;
  }
  if (DAT_10007f3c == 1) {
    if (param_7 == 0) {
      param_7 = DAT_10007f2c;
    }
    iVar1 = MultiByteToWideChar(param_7,(-(uint)(param_8 != 0) & 8) + 1,param_3,param_4,(LPWSTR)0x0,
                                0);
    if (iVar1 == 0) {
      ExceptionList = local_14;
      return 0;
    }
    local_8 = 0;
    FUN_10005580(unaff_DI);
    local_8 = 0xffffffff;
    if (&uStack00000000 == (undefined1 *)0x3c) {
      ExceptionList = local_14;
      return 0;
    }
    iVar2 = MultiByteToWideChar(param_7,1,param_3,param_4,aWStack_2e + -7,iVar1);
    if (iVar2 == 0) {
      ExceptionList = local_14;
      return 0;
    }
    iVar2 = LCMapStringW(param_1,param_2,aWStack_2e + -7,iVar1,(LPWSTR)0x0,0);
    if (iVar2 == 0) {
      ExceptionList = local_14;
      return 0;
    }
    if ((param_2 & 0x400) == 0) {
      local_8 = 1;
      FUN_10005580(unaff_DI);
      local_8 = 0xffffffff;
      if (&uStack00000000 == (undefined1 *)0x3c) {
        ExceptionList = local_14;
        return 0;
      }
      iVar1 = LCMapStringW(param_1,param_2,aWStack_2e + -7,iVar1,aWStack_2e + -7,iVar2);
      if (iVar1 == 0) {
        ExceptionList = local_14;
        return 0;
      }
      if (param_6 == 0) {
        param_6 = 0;
        param_5 = (LPWSTR)0x0;
      }
      iVar2 = WideCharToMultiByte(param_7,0x220,aWStack_2e + -7,iVar2,(LPSTR)param_5,param_6,
                                  (LPCSTR)0x0,(LPBOOL)0x0);
      iVar1 = iVar2;
    }
    else {
      if (param_6 == 0) {
        ExceptionList = local_14;
        return iVar2;
      }
      if (param_6 < iVar2) {
        ExceptionList = local_14;
        return 0;
      }
      iVar1 = LCMapStringW(param_1,param_2,aWStack_2e + -7,iVar1,param_5,param_6);
    }
    if (iVar1 != 0) {
      ExceptionList = local_14;
      return iVar2;
    }
  }
  ExceptionList = local_14;
  return 0;
}


