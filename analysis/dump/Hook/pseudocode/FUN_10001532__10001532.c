// Program: Hook.dll
// Function: FUN_10001532
// Entry: 10001532
// Body: 10001532 - 1000160a
// Signature: undefined4 FUN_10001532(undefined4 param_1, int param_2)


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN_10001532(undefined4 param_1,int param_2)

{
  int iVar1;
  undefined4 uVar2;
  
  if (param_2 == 1) {
    DAT_10007d48 = GetVersion();
    iVar1 = FUN_100028ef(1);
    if (iVar1 != 0) {
      _DAT_10007d54 = DAT_10007d48 >> 8 & 0xff;
      _DAT_10007d50 = DAT_10007d48 & 0xff;
      DAT_10007d48 = DAT_10007d48 >> 0x10;
      _DAT_10007d4c = _DAT_10007d50 * 0x100 + _DAT_10007d54;
      iVar1 = FUN_1000211b();
      if (iVar1 != 0) {
        DAT_10009418 = GetCommandLineA();
        DAT_10007d34 = FUN_100027bd();
        FUN_100022a7();
        FUN_10002570();
        FUN_100024b7();
        FUN_10001ffd();
        DAT_10007d30 = DAT_10007d30 + 1;
        goto LAB_10001605;
      }
      FUN_1000292b();
    }
LAB_10001592:
    uVar2 = 0;
  }
  else {
    if (param_2 == 0) {
      if (DAT_10007d30 < 1) goto LAB_10001592;
      DAT_10007d30 = DAT_10007d30 + -1;
      if (DAT_10007d80 == 0) {
        FUN_1000203b();
      }
      FUN_10002463();
      FUN_1000216f();
      FUN_1000292b();
    }
    else if (param_2 == 3) {
      FUN_10002207((LPVOID)0x0);
    }
LAB_10001605:
    uVar2 = 1;
  }
  return uVar2;
}


