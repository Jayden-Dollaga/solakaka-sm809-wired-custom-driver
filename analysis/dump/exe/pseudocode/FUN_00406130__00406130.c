// Program: SM809 mouse Software.exe
// Function: FUN_00406130
// Entry: 00406130
// Body: 00406130 - 0040654a
// Signature: int * FUN_00406130(void * this, int * param_1)


int * __thiscall FUN_00406130(void *this,int *param_1)

{
  int iVar1;
  int *piVar2;
  int *piVar3;
  int *piVar4;
  int *piVar5;
  char cVar6;
  int *piVar7;
  
  piVar5 = (int *)param_1[2];
  piVar4 = param_1 + 2;
  if (*(char *)((int)piVar5 + 0xd) == '\0') {
    cVar6 = *(char *)(*piVar5 + 0xd);
    piVar3 = (int *)*piVar5;
    while (cVar6 == '\0') {
      cVar6 = *(char *)(*piVar3 + 0xd);
      piVar5 = piVar3;
      piVar3 = (int *)*piVar3;
    }
  }
  else {
    cVar6 = *(char *)(param_1[1] + 0xd);
    piVar7 = (int *)param_1[1];
    piVar3 = param_1;
    while ((piVar5 = piVar7, cVar6 == '\0' && (piVar3 == (int *)piVar5[2]))) {
      cVar6 = *(char *)(piVar5[1] + 0xd);
      piVar7 = (int *)piVar5[1];
      piVar3 = piVar5;
    }
  }
  piVar3 = (int *)*param_1;
  piVar7 = (int *)*piVar4;
  if (*(char *)((int)piVar3 + 0xd) == '\0') {
    if (*(char *)(*piVar4 + 0xd) == '\0') {
      piVar7 = (int *)piVar5[2];
      if (piVar5 != param_1) {
        piVar3[1] = (int)piVar5;
        *piVar5 = *param_1;
        if (piVar5 == (int *)*piVar4) {
          piVar3 = piVar5;
        }
        else {
          piVar3 = (int *)piVar5[1];
          if (*(char *)((int)piVar7 + 0xd) == '\0') {
            piVar7[1] = (int)piVar3;
          }
          *piVar3 = (int)piVar7;
          piVar5[2] = *piVar4;
          *(int **)(*piVar4 + 4) = piVar5;
        }
        if (*(int **)(*(int *)this + 4) == param_1) {
          *(int **)(*(int *)this + 4) = piVar5;
        }
        else {
          piVar4 = (int *)param_1[1];
          if ((int *)*piVar4 == param_1) {
            *piVar4 = (int)piVar5;
          }
          else {
            piVar4[2] = (int)piVar5;
          }
        }
        cVar6 = (char)piVar5[3];
        piVar5[1] = param_1[1];
        *(char *)(piVar5 + 3) = (char)param_1[3];
        *(char *)(param_1 + 3) = cVar6;
        goto LAB_004062ae;
      }
    }
    else {
      piVar7 = piVar3;
    }
  }
  piVar3 = (int *)param_1[1];
  if (*(char *)((int)piVar7 + 0xd) == '\0') {
    piVar7[1] = (int)piVar3;
  }
  if (*(int **)(*(int *)this + 4) == param_1) {
    *(int **)(*(int *)this + 4) = piVar7;
  }
  else if ((int *)*piVar3 == param_1) {
    *piVar3 = (int)piVar7;
  }
  else {
    piVar3[2] = (int)piVar7;
  }
  if ((int *)**(int **)this == param_1) {
    if (*(char *)((int)piVar7 + 0xd) == '\0') {
      cVar6 = *(char *)(*piVar7 + 0xd);
      piVar4 = (int *)*piVar7;
      piVar5 = piVar7;
      while (piVar2 = piVar4, cVar6 == '\0') {
        piVar4 = (int *)*piVar2;
        cVar6 = *(char *)((int)piVar4 + 0xd);
        piVar5 = piVar2;
      }
    }
    else {
      piVar5 = piVar3;
    }
    **(int **)this = (int)piVar5;
  }
  iVar1 = *(int *)this;
  if (*(int **)(iVar1 + 8) == param_1) {
    if (*(char *)((int)piVar7 + 0xd) != '\0') {
      *(int **)(iVar1 + 8) = piVar3;
      cVar6 = (char)param_1[3];
      goto LAB_004062ae;
    }
    cVar6 = *(char *)(piVar7[2] + 0xd);
    piVar4 = (int *)piVar7[2];
    piVar5 = piVar7;
    while (piVar2 = piVar4, cVar6 == '\0') {
      piVar4 = (int *)piVar2[2];
      cVar6 = *(char *)((int)piVar4 + 0xd);
      piVar5 = piVar2;
    }
    *(int **)(iVar1 + 8) = piVar5;
  }
  cVar6 = (char)param_1[3];
LAB_004062ae:
  if (cVar6 == '\x01') {
    if (piVar7 != *(int **)(*(int *)this + 4)) {
      while( true ) {
        piVar4 = piVar3;
        if ((char)piVar7[3] != '\x01') break;
        piVar5 = (int *)*piVar4;
        if (piVar7 == piVar5) {
          piVar5 = (int *)piVar4[2];
          if ((char)piVar5[3] == '\0') {
            *(undefined1 *)(piVar5 + 3) = 1;
            piVar5 = (int *)piVar4[2];
            *(undefined1 *)(piVar4 + 3) = 0;
            piVar4[2] = *piVar5;
            if (*(char *)(*piVar5 + 0xd) == '\0') {
              *(int **)(*piVar5 + 4) = piVar4;
            }
            piVar5[1] = piVar4[1];
            if (piVar4 == *(int **)(*(int *)this + 4)) {
              *(int **)(*(int *)this + 4) = piVar5;
            }
            else {
              piVar3 = (int *)piVar4[1];
              if (piVar4 == (int *)*piVar3) {
                *piVar3 = (int)piVar5;
              }
              else {
                piVar3[2] = (int)piVar5;
              }
            }
            *piVar5 = (int)piVar4;
            piVar4[1] = (int)piVar5;
            piVar5 = (int *)piVar4[2];
          }
          if (*(char *)((int)piVar5 + 0xd) == '\0') {
            if ((*(char *)(*piVar5 + 0xc) == '\x01') && (*(char *)(piVar5[2] + 0xc) == '\x01'))
            goto LAB_004063f0;
            if (*(char *)(piVar5[2] + 0xc) == '\x01') {
              *(undefined1 *)(*piVar5 + 0xc) = 1;
              iVar1 = *piVar5;
              *(undefined1 *)(piVar5 + 3) = 0;
              *piVar5 = *(int *)(iVar1 + 8);
              if (*(char *)(*(int *)(iVar1 + 8) + 0xd) == '\0') {
                *(int **)(*(int *)(iVar1 + 8) + 4) = piVar5;
              }
              *(int *)(iVar1 + 4) = piVar5[1];
              if (piVar5 == *(int **)(*(int *)this + 4)) {
                *(int *)(*(int *)this + 4) = iVar1;
              }
              else {
                piVar3 = (int *)piVar5[1];
                if (piVar5 == (int *)piVar3[2]) {
                  piVar3[2] = iVar1;
                }
                else {
                  *piVar3 = iVar1;
                }
              }
              *(int **)(iVar1 + 8) = piVar5;
              piVar5[1] = iVar1;
              piVar5 = (int *)piVar4[2];
            }
            *(char *)(piVar5 + 3) = (char)piVar4[3];
            *(undefined1 *)(piVar4 + 3) = 1;
            *(undefined1 *)(piVar5[2] + 0xc) = 1;
            piVar5 = (int *)piVar4[2];
            piVar4[2] = *piVar5;
            if (*(char *)(*piVar5 + 0xd) == '\0') {
              *(int **)(*piVar5 + 4) = piVar4;
            }
            piVar5[1] = piVar4[1];
            if (piVar4 == *(int **)(*(int *)this + 4)) {
              *(int **)(*(int *)this + 4) = piVar5;
              *piVar5 = (int)piVar4;
              piVar4[1] = (int)piVar5;
            }
            else {
              piVar3 = (int *)piVar4[1];
              if (piVar4 == (int *)*piVar3) {
                *piVar3 = (int)piVar5;
                *piVar5 = (int)piVar4;
                piVar4[1] = (int)piVar5;
              }
              else {
                piVar3[2] = (int)piVar5;
                *piVar5 = (int)piVar4;
                piVar4[1] = (int)piVar5;
              }
            }
            break;
          }
        }
        else {
          if ((char)piVar5[3] == '\0') {
            *(undefined1 *)(piVar5 + 3) = 1;
            iVar1 = *piVar4;
            *(undefined1 *)(piVar4 + 3) = 0;
            *piVar4 = *(int *)(iVar1 + 8);
            if (*(char *)(*(int *)(iVar1 + 8) + 0xd) == '\0') {
              *(int **)(*(int *)(iVar1 + 8) + 4) = piVar4;
            }
            *(int *)(iVar1 + 4) = piVar4[1];
            if (piVar4 == *(int **)(*(int *)this + 4)) {
              *(int *)(*(int *)this + 4) = iVar1;
            }
            else {
              piVar5 = (int *)piVar4[1];
              if (piVar4 == (int *)piVar5[2]) {
                piVar5[2] = iVar1;
              }
              else {
                *piVar5 = iVar1;
              }
            }
            *(int **)(iVar1 + 8) = piVar4;
            piVar4[1] = iVar1;
            piVar5 = (int *)*piVar4;
          }
          if (*(char *)((int)piVar5 + 0xd) == '\0') {
            if ((*(char *)(piVar5[2] + 0xc) != '\x01') || (*(char *)(*piVar5 + 0xc) != '\x01')) {
              if (*(char *)(*piVar5 + 0xc) == '\x01') {
                *(undefined1 *)(piVar5[2] + 0xc) = 1;
                piVar3 = (int *)piVar5[2];
                *(undefined1 *)(piVar5 + 3) = 0;
                piVar5[2] = *piVar3;
                if (*(char *)(*piVar3 + 0xd) == '\0') {
                  *(int **)(*piVar3 + 4) = piVar5;
                }
                piVar3[1] = piVar5[1];
                if (piVar5 == *(int **)(*(int *)this + 4)) {
                  *(int **)(*(int *)this + 4) = piVar3;
                }
                else {
                  piVar2 = (int *)piVar5[1];
                  if (piVar5 == (int *)*piVar2) {
                    *piVar2 = (int)piVar3;
                  }
                  else {
                    piVar2[2] = (int)piVar3;
                  }
                }
                *piVar3 = (int)piVar5;
                piVar5[1] = (int)piVar3;
                piVar5 = (int *)*piVar4;
              }
              *(char *)(piVar5 + 3) = (char)piVar4[3];
              *(undefined1 *)(piVar4 + 3) = 1;
              *(undefined1 *)(*piVar5 + 0xc) = 1;
              iVar1 = *piVar4;
              *piVar4 = *(int *)(iVar1 + 8);
              if (*(char *)(*(int *)(iVar1 + 8) + 0xd) == '\0') {
                *(int **)(*(int *)(iVar1 + 8) + 4) = piVar4;
              }
              *(int *)(iVar1 + 4) = piVar4[1];
              if (piVar4 == *(int **)(*(int *)this + 4)) {
                *(int *)(*(int *)this + 4) = iVar1;
                *(int **)(iVar1 + 8) = piVar4;
                piVar4[1] = iVar1;
              }
              else {
                piVar5 = (int *)piVar4[1];
                if (piVar4 == (int *)piVar5[2]) {
                  piVar5[2] = iVar1;
                  *(int **)(iVar1 + 8) = piVar4;
                  piVar4[1] = iVar1;
                }
                else {
                  *piVar5 = iVar1;
                  *(int **)(iVar1 + 8) = piVar4;
                  piVar4[1] = iVar1;
                }
              }
              break;
            }
LAB_004063f0:
            *(undefined1 *)(piVar5 + 3) = 0;
          }
        }
        piVar3 = (int *)piVar4[1];
        piVar7 = piVar4;
        if (piVar4 == *(int **)(*(int *)this + 4)) break;
      }
    }
    *(undefined1 *)(piVar7 + 3) = 1;
  }
  if (*(int *)((int)this + 4) != 0) {
    *(int *)((int)this + 4) = *(int *)((int)this + 4) + -1;
  }
  return param_1;
}


