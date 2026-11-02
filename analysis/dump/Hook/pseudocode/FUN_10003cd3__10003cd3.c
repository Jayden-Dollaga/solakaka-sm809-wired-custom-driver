// Program: Hook.dll
// Function: FUN_10003cd3
// Entry: 10003cd3
// Body: 10003cd3 - 10003cfd
// Signature: uint FUN_10003cd3(int param_1)


uint __cdecl FUN_10003cd3(int param_1)

{
  uint uVar1;
  
  uVar1 = DAT_1000809c;
  while( true ) {
    if (DAT_1000809c + DAT_10008098 * 0x14 <= uVar1) {
      return 0;
    }
    if ((uint)(param_1 - *(int *)(uVar1 + 0xc)) < 0x100000) break;
    uVar1 = uVar1 + 0x14;
  }
  return uVar1;
}


