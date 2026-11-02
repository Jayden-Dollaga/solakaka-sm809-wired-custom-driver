// Program: MSDriver.dll
// Function: FUN_10003f48
// Entry: 10003f48
// Body: 10003f48 - 10003fe0
// Signature: undefined FUN_10003f48(void)


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_10003f48(void)

{
  undefined4 *puVar1;
  byte *pbVar2;
  int local_c;
  int local_8;
  
  if (DAT_1000b5c8 == 0) {
    FUN_10005328();
  }
  GetModuleFileNameA((HMODULE)0x0,&DAT_10009fbc,0x104);
  _DAT_10009fa8 = &DAT_10009fbc;
  pbVar2 = &DAT_10009fbc;
  if (*DAT_1000b5f4 != 0) {
    pbVar2 = DAT_1000b5f4;
  }
  FUN_10003fe1(pbVar2,(undefined4 *)0x0,(byte *)0x0,&local_8,&local_c);
  puVar1 = _malloc(local_c + local_8 * 4);
  if (puVar1 == (undefined4 *)0x0) {
    __amsg_exit(8);
  }
  FUN_10003fe1(pbVar2,puVar1,(byte *)(puVar1 + local_8),&local_8,&local_c);
  _DAT_10009f90 = puVar1;
  _DAT_10009f8c = local_8 + -1;
  return;
}


