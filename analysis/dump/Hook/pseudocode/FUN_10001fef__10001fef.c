// Program: Hook.dll
// Function: FUN_10001fef
// Entry: 10001fef
// Body: 10001fef - 10001ffc
// Signature: undefined4 FUN_10001fef(int * param_1)


undefined4 __cdecl FUN_10001fef(int *param_1)

{
  *param_1 = *param_1 + 4;
  return CONCAT22((short)((uint)*param_1 >> 0x10),*(undefined2 *)(*param_1 + -4));
}


