// Program: MSDriver.dll
// Function: FUN_10003972
// Entry: 10003972
// Body: 10003972 - 100039a9
// Signature: undefined FUN_10003972(char * param_1, int param_2, int * param_3, int * param_4)


void __cdecl FUN_10003972(char *param_1,int param_2,int *param_3,int *param_4)

{
  char cVar1;
  
  if (0 < param_2) {
    do {
      param_2 = param_2 + -1;
      cVar1 = *param_1;
      param_1 = param_1 + 1;
      FUN_1000390c((int)cVar1,param_3,param_4);
      if (*param_4 == -1) {
        return;
      }
    } while (0 < param_2);
  }
  return;
}


