// Program: SM809 mouse Software.exe
// Function: FUN_0040fab0
// Entry: 0040fab0
// Body: 0040fab0 - 0040fadd
// Signature: undefined FUN_0040fab0(void * this, int param_1)


void __thiscall FUN_0040fab0(void *this,int param_1)

{
  if ((*(int *)(param_1 + 0x108) == *(int *)((int)this + 0x35c)) &&
     (*(int *)((int)this + 0x2a8) != 0)) {
    (**(code **)((int)this + 800))(1);
  }
  return;
}


