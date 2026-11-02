// Program: Hook.dll
// Function: FUN_10001fdf
// Entry: 10001fdf
// Body: 10001fdf - 10001fee
// Signature: undefined8 FUN_10001fdf(int * param_1)


undefined8 __cdecl FUN_10001fdf(int *param_1)

{
  *param_1 = *param_1 + 8;
  return *(undefined8 *)(*param_1 + -8);
}


