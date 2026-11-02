// Program: SM809 mouse Software.exe
// Function: FUN_00406020
// Entry: 00406020
// Body: 00406020 - 00406122
// Signature: undefined FUN_00406020(void * this, undefined4 * param_1)


void __thiscall FUN_00406020(void *this,undefined4 *param_1)

{
  int *piVar1;
  bool bVar2;
  code *pcVar3;
  uint uVar4;
  int *piVar5;
  int *piVar6;
  int *piVar7;
  uint uVar8;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_004215ed;
  local_10 = ExceptionList;
  uVar4 = DAT_00432008 ^ (int)register0x00000010 - 4U;
  ExceptionList = &local_10;
  if (param_1 != (undefined4 *)0x0) {
    piVar1 = *(int **)((int)this + 4);
    uVar8 = 0;
    piVar7 = (int *)piVar1[1];
    piVar6 = piVar1;
    if (*(char *)((int)piVar7 + 0xd) == '\0') {
      piVar5 = piVar7;
      do {
        piVar7 = piVar5;
        bVar2 = *(int *)((int)this + 0xc) <= piVar7[4];
        if (bVar2) {
          piVar5 = (int *)*piVar7;
          piVar6 = piVar7;
        }
        else {
          piVar5 = (int *)piVar7[2];
        }
        uVar8 = (uint)bVar2;
      } while (*(char *)((int)piVar5 + 0xd) == '\0');
    }
    if ((*(char *)((int)piVar6 + 0xd) != '\0') || (*(int *)((int)this + 0xc) < piVar6[4])) {
      if (*(int *)((int)this + 8) == 0xaaaaaaa) {
        FUN_00405de0();
        pcVar3 = (code *)swi(3);
        (*pcVar3)();
        return;
      }
      local_8 = 0;
      piVar6 = operator_new(0x18);
      local_8 = 0xffffffff;
      piVar6[4] = *(int *)((int)this + 0xc);
      piVar6[5] = 0;
      *piVar6 = (int)piVar1;
      piVar6[1] = (int)piVar1;
      piVar6[2] = (int)piVar1;
      *(undefined2 *)(piVar6 + 3) = 0;
      piVar6 = Insert_node((void *)((int)this + 4),piVar7,uVar8,piVar6);
    }
    piVar6[5] = (int)param_1;
    (**(code **)*param_1)(this,uVar4);
    *(int *)((int)this + 0xc) = *(int *)((int)this + 0xc) + 1;
  }
  ExceptionList = local_10;
  return;
}


