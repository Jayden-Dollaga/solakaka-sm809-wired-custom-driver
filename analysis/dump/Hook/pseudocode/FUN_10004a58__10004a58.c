// Program: Hook.dll
// Function: FUN_10004a58
// Entry: 10004a58
// Body: 10004a58 - 10004a72
// Signature: undefined4 FUN_10004a58(undefined4 param_1)


undefined4 __cdecl FUN_10004a58(undefined4 param_1)

{
  int iVar1;
  
  if (DAT_10007f34 != (code *)0x0) {
    iVar1 = (*DAT_10007f34)(param_1);
    if (iVar1 != 0) {
      return 1;
    }
  }
  return 0;
}


