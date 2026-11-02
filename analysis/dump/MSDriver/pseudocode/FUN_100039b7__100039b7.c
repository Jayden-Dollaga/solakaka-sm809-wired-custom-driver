// Program: MSDriver.dll
// Function: FUN_100039b7
// Entry: 100039b7
// Body: 100039b7 - 100039c6
// Signature: undefined8 FUN_100039b7(int * param_1)


undefined8 __cdecl FUN_100039b7(int *param_1)

{
  *param_1 = *param_1 + 8;
  return *(undefined8 *)(*param_1 + -8);
}


