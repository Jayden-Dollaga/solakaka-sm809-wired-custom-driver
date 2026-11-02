// Program: Hook.dll
// Function: FUN_10001f9a
// Entry: 10001f9a
// Body: 10001f9a - 10001fd1
// Signature: undefined FUN_10001f9a(char * param_1, int param_2, int * param_3, int * param_4)


void __cdecl FUN_10001f9a(char *param_1,int param_2,int *param_3,int *param_4)

{
  char cVar1;
  
  if (0 < param_2) {
    do {
      param_2 = param_2 + -1;
      cVar1 = *param_1;
      param_1 = param_1 + 1;
      FUN_10001f34((int)cVar1,param_3,param_4);
      if (*param_4 == -1) {
        return;
      }
    } while (0 < param_2);
  }
  return;
}


