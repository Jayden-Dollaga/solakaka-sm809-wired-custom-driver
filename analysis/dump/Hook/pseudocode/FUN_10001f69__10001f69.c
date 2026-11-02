// Program: Hook.dll
// Function: FUN_10001f69
// Entry: 10001f69
// Body: 10001f69 - 10001f99
// Signature: undefined FUN_10001f69(uint param_1, int param_2, int * param_3, int * param_4)


void __cdecl FUN_10001f69(uint param_1,int param_2,int *param_3,int *param_4)

{
  do {
    if (param_2 < 1) {
      return;
    }
    param_2 = param_2 + -1;
    FUN_10001f34(param_1,param_3,param_4);
  } while (*param_4 != -1);
  return;
}


