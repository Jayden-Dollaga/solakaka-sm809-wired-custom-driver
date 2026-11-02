// Program: SM809 mouse Software.exe
// Function: FUN_00406790
// Entry: 00406790
// Body: 00406790 - 004067bb
// Signature: undefined4 * FUN_00406790(void * this, byte param_1)


undefined4 * __thiscall FUN_00406790(void *this,byte param_1)

{
  *(undefined ***)this = ObserverImpl<int,SkinChangedParam>::vftable;
  ~_Tree<>((int *)((int)this + 4));
  if ((param_1 & 1) != 0) {
    FUN_0041feb7(this);
  }
  return this;
}


