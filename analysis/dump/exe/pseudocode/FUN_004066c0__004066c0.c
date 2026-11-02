// Program: SM809 mouse Software.exe
// Function: FUN_004066c0
// Entry: 004066c0
// Body: 004066c0 - 00406785
// Signature: undefined4 FUN_004066c0(int param_1, undefined4 param_2, undefined4 param_3, CDuiString param_4)


undefined4 __thiscall
FUN_004066c0(int param_1,undefined4 param_2,undefined4 param_3,CDuiString param_4)

{
  char cVar1;
  int *piVar2;
  int *piVar3;
  int *piVar4;
  CDuiString aCStack_ac [132];
  int iStack_28;
  uint uStack_24;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  puStack_c = &LAB_0042161d;
  local_10 = ExceptionList;
  uStack_24 = DAT_00432008 ^ (uint)(aCStack_ac + 0xa8);
  ExceptionList = &local_10;
  local_8 = 0;
  piVar4 = (int *)**(int **)(param_1 + 4);
  if (piVar4 != *(int **)(param_1 + 4)) {
    do {
      piVar2 = (int *)piVar4[5];
      iStack_28 = param_1;
      DuiLib::CDuiString::CDuiString(aCStack_ac,&param_4);
      (**(code **)(*piVar2 + 0xc))();
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
  iStack_28 = 0x406770;
  DuiLib::CDuiString::~CDuiString(&param_4);
  ExceptionList = local_10;
  return 0;
}


