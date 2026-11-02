// Program: SM809 mouse Software.exe
// Function: FUN_00406550
// Entry: 00406550
// Body: 00406550 - 004065d0
// Signature: undefined FUN_00406550(void * this, int param_1)


void __thiscall FUN_00406550(void *this,int param_1)

{
  char cVar1;
  int *piVar2;
  int *piVar3;
  int *piVar4;
  int *piVar5;
  
  if (param_1 != 0) {
    piVar5 = *(int **)((int)this + 4);
    piVar4 = (int *)*piVar5;
    if (piVar4 != piVar5) {
      while (piVar4[5] != param_1) {
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
        if (piVar4 == piVar5) {
          return;
        }
      }
      piVar5 = FUN_00406130((int *)((int)this + 4),piVar4);
      FUN_0041feb7(piVar5);
    }
  }
  return;
}


