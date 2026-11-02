// Program: SM809 mouse Software.exe
// Function: FUN_0041d620
// Entry: 0041d620
// Body: 0041d620 - 0041d68c
// Signature: undefined FUN_0041d620(void * this, int param_1)


void __thiscall FUN_0041d620(void *this,int param_1)

{
  undefined4 *puVar1;
  int iVar2;
  
  if (0 < param_1) {
    puVar1 = (undefined4 *)((int)this + 0x88);
    iVar2 = param_1;
    do {
      (**(code **)(*(int *)*puVar1 + 0xf8))(1);
      puVar1 = puVar1 + 1;
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
  }
  if (param_1 < 8) {
    puVar1 = (undefined4 *)((int)this + (param_1 + 0x22) * 4);
    iVar2 = 8 - param_1;
    do {
      (**(code **)(*(int *)*puVar1 + 0xf8))(0);
      puVar1 = puVar1 + 1;
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
  }
  return;
}


