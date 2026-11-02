// Program: MSDriver.dll
// Function: FUN_100039c7
// Entry: 100039c7
// Body: 100039c7 - 100039d4
// Signature: undefined4 FUN_100039c7(int * param_1)


undefined4 __cdecl FUN_100039c7(int *param_1)

{
  *param_1 = *param_1 + 4;
  return CONCAT22((short)((uint)*param_1 >> 0x10),*(undefined2 *)(*param_1 + -4));
}


