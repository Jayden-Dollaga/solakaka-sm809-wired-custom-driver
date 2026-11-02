// Program: Hook.dll
// Function: FUN_10001fd2
// Entry: 10001fd2
// Body: 10001fd2 - 10001fde
// Signature: undefined4 FUN_10001fd2(int * param_1)


undefined4 __cdecl FUN_10001fd2(int *param_1)

{
  *param_1 = *param_1 + 4;
  return *(undefined4 *)(*param_1 + -4);
}


