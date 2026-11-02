// Program: SM809 mouse Software.exe
// Function: FUN_00405d80
// Entry: 00405d80
// Body: 00405d80 - 00405d8d
// Signature: char * FUN_00405d80(int param_1)


char * __fastcall FUN_00405d80(int param_1)

{
  char *pcVar1;
  
  pcVar1 = "Unknown exception";
  if (*(char **)(param_1 + 4) != (char *)0x0) {
    pcVar1 = *(char **)(param_1 + 4);
  }
  return pcVar1;
}


