// Program: SM809 mouse Software.exe
// Function: FUN_0041c0d0
// Entry: 0041c0d0
// Body: 0041c0d0 - 0041c133
// Signature: undefined FUN_0041c0d0(int param_1)


void __fastcall FUN_0041c0d0(int param_1)

{
  char cVar1;
  int *piVar2;
  int *piVar3;
  int *piVar4;
  
  piVar4 = (int *)**(int **)(param_1 + 4);
  if (piVar4 != *(int **)(param_1 + 4)) {
    do {
      (**(code **)(*(int *)piVar4[5] + 4))(param_1);
      piVar2 = (int *)piVar4[2];
      if (*(char *)((int)piVar2 + 0xd) == '\0') {
        cVar1 = *(char *)(*piVar2 + 0xd);
        piVar4 = piVar2;
        piVar2 = (int *)*piVar2;
        while (cVar1 == '\0') {
          cVar1 = *(char *)(*piVar2 + 0xd);
          piVar4 = piVar2;
          piVar2 = (int *)*piVar2;
        }
      }
      else {
        cVar1 = *(char *)(piVar4[1] + 0xd);
        piVar3 = (int *)piVar4[1];
        piVar2 = piVar4;
        while ((piVar4 = piVar3, cVar1 == '\0' && (piVar2 == (int *)piVar4[2]))) {
          cVar1 = *(char *)(piVar4[1] + 0xd);
          piVar3 = (int *)piVar4[1];
          piVar2 = piVar4;
        }
      }
    } while (piVar4 != *(int **)(param_1 + 4));
  }
  return;
}


