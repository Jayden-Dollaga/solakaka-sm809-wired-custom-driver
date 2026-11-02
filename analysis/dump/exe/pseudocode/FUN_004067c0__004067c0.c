// Program: SM809 mouse Software.exe
// Function: FUN_004067c0
// Entry: 004067c0
// Body: 004067c0 - 004067fa
// Signature: undefined FUN_004067c0(undefined4 param_1, int * param_2)


void FUN_004067c0(undefined4 param_1,int *param_2)

{
  char cVar1;
  int *piVar2;
  
  cVar1 = *(char *)((int)param_2 + 0xd);
  while (cVar1 == '\0') {
    FUN_004067c0(param_1,(int *)param_2[2]);
    piVar2 = (int *)*param_2;
    FUN_0041feb7(param_2);
    param_2 = piVar2;
    cVar1 = *(char *)((int)piVar2 + 0xd);
  }
  return;
}


