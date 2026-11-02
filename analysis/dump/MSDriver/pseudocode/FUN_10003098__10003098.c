// Program: MSDriver.dll
// Function: FUN_10003098
// Entry: 10003098
// Body: 10003098 - 100030b2
// Signature: undefined4 FUN_10003098(undefined4 param_1)


undefined4 __cdecl FUN_10003098(undefined4 param_1)

{
  int iVar1;
  
  if (DAT_10009f70 != (code *)0x0) {
    iVar1 = (*DAT_10009f70)(param_1);
    if (iVar1 != 0) {
      return 1;
    }
  }
  return 0;
}


