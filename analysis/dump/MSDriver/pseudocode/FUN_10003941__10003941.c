// Program: MSDriver.dll
// Function: FUN_10003941
// Entry: 10003941
// Body: 10003941 - 10003971
// Signature: undefined FUN_10003941(uint param_1, int param_2, int * param_3, int * param_4)


void __cdecl FUN_10003941(uint param_1,int param_2,int *param_3,int *param_4)

{
  do {
    if (param_2 < 1) {
      return;
    }
    param_2 = param_2 + -1;
    FUN_1000390c(param_1,param_3,param_4);
  } while (*param_4 != -1);
  return;
}


