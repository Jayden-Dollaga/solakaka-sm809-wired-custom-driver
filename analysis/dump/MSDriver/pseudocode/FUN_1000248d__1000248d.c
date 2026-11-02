// Program: MSDriver.dll
// Function: FUN_1000248d
// Entry: 1000248d
// Body: 1000248d - 10002565
// Signature: undefined4 FUN_1000248d(undefined4 param_1, int param_2)


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN_1000248d(undefined4 param_1,int param_2)

{
  int iVar1;
  undefined4 uVar2;
  
  if (param_2 == 1) {
    DAT_10009f7c = GetVersion();
    iVar1 = FUN_10002636(1);
    if (iVar1 != 0) {
      _DAT_10009f88 = DAT_10009f7c >> 8 & 0xff;
      _DAT_10009f84 = DAT_10009f7c & 0xff;
      DAT_10009f7c = DAT_10009f7c >> 0x10;
      _DAT_10009f80 = _DAT_10009f84 * 0x100 + _DAT_10009f88;
      iVar1 = FUN_10003af3();
      if (iVar1 != 0) {
        DAT_1000b5f4 = GetCommandLineA();
        DAT_10009f00 = FUN_10004195();
        FUN_10003c7f();
        FUN_10003f48();
        FUN_10003e8f();
        FUN_100039d5();
        DAT_10009efc = DAT_10009efc + 1;
        goto LAB_10002560;
      }
      FUN_10002672();
    }
LAB_100024ed:
    uVar2 = 0;
  }
  else {
    if (param_2 == 0) {
      if (DAT_10009efc < 1) goto LAB_100024ed;
      DAT_10009efc = DAT_10009efc + -1;
      if (DAT_10009fb4 == 0) {
        FUN_10003a13();
      }
      FUN_10003e3b();
      FUN_10003b47();
      FUN_10002672();
    }
    else if (param_2 == 3) {
      FUN_10003bdf((LPVOID)0x0);
    }
LAB_10002560:
    uVar2 = 1;
  }
  return uVar2;
}


