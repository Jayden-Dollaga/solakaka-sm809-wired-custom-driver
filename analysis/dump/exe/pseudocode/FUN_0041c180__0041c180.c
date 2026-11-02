// Program: SM809 mouse Software.exe
// Function: FUN_0041c180
// Entry: 0041c180
// Body: 0041c180 - 0041c1ab
// Signature: undefined4 * FUN_0041c180(void * this, byte param_1)


undefined4 * __thiscall FUN_0041c180(void *this,byte param_1)

{
  *(undefined ***)this = ReceiverImpl<int,SkinChangedParam>::vftable;
  ~_Tree<>((int *)((int)this + 4));
  if ((param_1 & 1) != 0) {
    FUN_0041feb7(this);
  }
  return this;
}


