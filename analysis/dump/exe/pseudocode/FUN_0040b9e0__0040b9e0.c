// Program: SM809 mouse Software.exe
// Function: FUN_0040b9e0
// Entry: 0040b9e0
// Body: 0040b9e0 - 0040ba4c
// Signature: undefined FUN_0040b9e0(void * this, int param_1)


void __thiscall FUN_0040b9e0(void *this,int param_1)

{
  undefined4 *puVar1;
  int iVar2;
  
  if (0 < param_1) {
    puVar1 = (undefined4 *)((int)this + 0x1c8);
    iVar2 = param_1;
    do {
      (**(code **)(*(int *)*puVar1 + 0xf8))(1);
      puVar1 = puVar1 + 1;
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
  }
  if (param_1 < 0x1e) {
    puVar1 = (undefined4 *)((int)this + (param_1 + 0x72) * 4);
    iVar2 = 0x1e - param_1;
    do {
      (**(code **)(*(int *)*puVar1 + 0xf8))(0);
      puVar1 = puVar1 + 1;
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
  }
  return;
}


