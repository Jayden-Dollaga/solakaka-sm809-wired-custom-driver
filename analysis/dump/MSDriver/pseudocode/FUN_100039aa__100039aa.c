// Program: MSDriver.dll
// Function: FUN_100039aa
// Entry: 100039aa
// Body: 100039aa - 100039b6
// Signature: undefined4 FUN_100039aa(int * param_1)


undefined4 __cdecl FUN_100039aa(int *param_1)

{
  *param_1 = *param_1 + 4;
  return *(undefined4 *)(*param_1 + -4);
}


