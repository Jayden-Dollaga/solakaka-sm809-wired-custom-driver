// Program: SM809 mouse Software.exe
// Function: FUN_00406d20
// Entry: 00406d20
// Body: 00406d20 - 00406d98
// Signature: undefined FUN_00406d20(void * this, int param_1)


void __thiscall FUN_00406d20(void *this,int param_1)

{
  int *piVar1;
  undefined4 *puVar2;
  int iVar3;
  int local_c;
  
  piVar1 = (int *)((int)this + 0x20);
  local_c = 0x40;
  do {
    if (*(int *)(param_1 + 0x108) == *piVar1) {
      puVar2 = (undefined4 *)((int)this + 0x13c);
      iVar3 = 0x20;
      do {
        (**(code **)(*(int *)*puVar2 + 0xf8))(0);
        puVar2 = puVar2 + 1;
        iVar3 = iVar3 + -1;
      } while (iVar3 != 0);
      (**(code **)(**(int **)((int)this + 0x1bc) + 0xf8))(1);
    }
    piVar1 = piVar1 + 1;
    local_c = local_c + -1;
  } while (local_c != 0);
  return;
}


