// Program: SM809 mouse Software.exe
// Function: FUN_0041bfe0
// Entry: 0041bfe0
// Body: 0041bfe0 - 0041c0c6
// Signature: undefined FUN_0041bfe0(void * this, int param_1)


void __thiscall FUN_0041bfe0(void *this,int param_1)

{
  int *piVar1;
  bool bVar2;
  code *pcVar3;
  int *piVar4;
  int *piVar5;
  uint uVar6;
  int *piVar7;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_0042372d;
  local_10 = ExceptionList;
  ExceptionList = &local_10;
  piVar1 = *(int **)((int)this + 4);
  uVar6 = 0;
  piVar7 = (int *)piVar1[1];
  piVar5 = piVar1;
  if (*(char *)((int)piVar7 + 0xd) == '\0') {
    piVar4 = piVar7;
    do {
      piVar7 = piVar4;
      bVar2 = *(int *)((int)this + 0xc) <= piVar7[4];
      if (bVar2) {
        piVar4 = (int *)*piVar7;
        piVar5 = piVar7;
      }
      else {
        piVar4 = (int *)piVar7[2];
      }
      uVar6 = (uint)bVar2;
    } while (*(char *)((int)piVar4 + 0xd) == '\0');
  }
  if ((*(char *)((int)piVar5 + 0xd) != '\0') || (*(int *)((int)this + 0xc) < piVar5[4])) {
    if (*(int *)((int)this + 8) == 0xaaaaaaa) {
      FUN_00405de0();
      pcVar3 = (code *)swi(3);
      (*pcVar3)();
      return;
    }
    local_8 = 0;
    piVar5 = operator_new(0x18);
    piVar5[4] = *(int *)((int)this + 0xc);
    piVar5[5] = 0;
    *piVar5 = (int)piVar1;
    piVar5[1] = (int)piVar1;
    piVar5[2] = (int)piVar1;
    *(undefined2 *)(piVar5 + 3) = 0;
    piVar5 = Insert_node((void *)((int)this + 4),piVar7,uVar6,piVar5);
  }
  piVar5[5] = param_1;
  *(int *)((int)this + 0xc) = *(int *)((int)this + 0xc) + 1;
  ExceptionList = local_10;
  return;
}


