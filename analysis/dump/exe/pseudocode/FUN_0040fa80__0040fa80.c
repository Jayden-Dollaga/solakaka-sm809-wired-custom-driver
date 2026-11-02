// Program: SM809 mouse Software.exe
// Function: FUN_0040fa80
// Entry: 0040fa80
// Body: 0040fa80 - 0040faad
// Signature: undefined FUN_0040fa80(void * this, int param_1)


void __thiscall FUN_0040fa80(void *this,int param_1)

{
  if ((*(int *)(param_1 + 0x108) == *(int *)((int)this + 0x35c)) &&
     (*(int *)((int)this + 0x2a8) != 0)) {
    (**(code **)((int)this + 800))(0);
  }
  return;
}


