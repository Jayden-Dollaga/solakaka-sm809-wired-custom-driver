// Program: MSDriver.dll
// Function: FUN_10002830
// Entry: 10002830
// Body: 10002830 - 1000285a
// Signature: uint FUN_10002830(int param_1)


uint __cdecl FUN_10002830(int param_1)

{
  uint uVar1;
  
  uVar1 = DAT_1000b5ec;
  while( true ) {
    if (DAT_1000b5ec + DAT_1000b5e8 * 0x14 <= uVar1) {
      return 0;
    }
    if ((uint)(param_1 - *(int *)(uVar1 + 0xc)) < 0x100000) break;
    uVar1 = uVar1 + 0x14;
  }
  return uVar1;
}


