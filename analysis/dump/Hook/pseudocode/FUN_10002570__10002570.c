// Program: Hook.dll
// Function: FUN_10002570
// Entry: 10002570
// Body: 10002570 - 10002608
// Signature: undefined FUN_10002570(void)


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_10002570(void)

{
  undefined4 *puVar1;
  byte *pbVar2;
  int local_c;
  int local_8;
  
  if (DAT_10009408 == 0) {
    FUN_10003938();
  }
  GetModuleFileNameA((HMODULE)0x0,&DAT_10007d88,0x104);
  _DAT_10007d74 = &DAT_10007d88;
  pbVar2 = &DAT_10007d88;
  if (*DAT_10009418 != 0) {
    pbVar2 = DAT_10009418;
  }
  FUN_10002609(pbVar2,(undefined4 *)0x0,(byte *)0x0,&local_8,&local_c);
  puVar1 = _malloc(local_c + local_8 * 4);
  if (puVar1 == (undefined4 *)0x0) {
    __amsg_exit(8);
  }
  FUN_10002609(pbVar2,puVar1,(byte *)(puVar1 + local_8),&local_8,&local_c);
  _DAT_10007d5c = puVar1;
  _DAT_10007d58 = local_8 + -1;
  return;
}


