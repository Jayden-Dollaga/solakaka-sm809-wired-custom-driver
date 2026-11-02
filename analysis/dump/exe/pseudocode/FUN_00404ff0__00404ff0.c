// Program: SM809 mouse Software.exe
// Function: FUN_00404ff0
// Entry: 00404ff0
// Body: 00404ff0 - 00405018
// Signature: int * FUN_00404ff0(void * this, byte param_1)


int * __thiscall FUN_00404ff0(void *this,byte param_1)

{
  int *piVar1;
  
  piVar1 = (int *)((int)this + -0x70);
  FUN_00402e30(piVar1);
  if ((param_1 & 1) != 0) {
    FUN_0041feb7(piVar1);
  }
  return piVar1;
}


