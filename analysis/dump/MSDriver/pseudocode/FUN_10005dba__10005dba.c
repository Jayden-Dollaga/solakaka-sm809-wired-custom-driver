// Program: MSDriver.dll
// Function: FUN_10005dba
// Entry: 10005dba
// Body: 10005dba - 10005de4
// Signature: int FUN_10005dba(char * param_1, int param_2)


int __cdecl FUN_10005dba(char *param_1,int param_2)

{
  char *pcVar1;
  int iVar2;
  
  iVar2 = param_2;
  for (pcVar1 = param_1; (iVar2 != 0 && (iVar2 = iVar2 + -1, *pcVar1 != '\0')); pcVar1 = pcVar1 + 1)
  {
  }
  if (*pcVar1 == '\0') {
    return (int)pcVar1 - (int)param_1;
  }
  return param_2;
}


