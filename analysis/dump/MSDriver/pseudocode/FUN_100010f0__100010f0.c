// Program: MSDriver.dll
// Function: FUN_100010f0
// Entry: 100010f0
// Body: 100010f0 - 10001175
// Signature: undefined4 FUN_100010f0(undefined4 param_1, int param_2)


undefined4 FUN_100010f0(undefined4 param_1,int param_2)

{
  DAT_1000c004 = param_1;
  if (param_2 == 0) {
    DeleteCriticalSection((LPCRITICAL_SECTION)&DAT_10009e98);
    FUN_100022da(DAT_10009eb0);
    if (DAT_1000c00c != 0) {
      SendMessageA(DAT_1000c000,0x10,0,0);
    }
  }
  else if (param_2 == 1) {
    DAT_10009eb0 = FUN_10002322(8,2);
    DAT_10009ebc = &DAT_10009eb8;
    DAT_10009eb8 = &DAT_10009eb8;
    InitializeCriticalSection((LPCRITICAL_SECTION)&DAT_10009e98);
    return 1;
  }
  return 1;
}


