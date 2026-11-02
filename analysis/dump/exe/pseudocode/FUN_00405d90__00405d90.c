// Program: SM809 mouse Software.exe
// Function: FUN_00405d90
// Entry: 00405d90
// Body: 00405d90 - 00405dbd
// Signature: undefined4 * FUN_00405d90(void * this, int param_1)


undefined4 * __thiscall FUN_00405d90(void *this,int param_1)

{
  *(undefined ***)this = std::exception::vftable;
  *(undefined8 *)((int)this + 4) = 0;
  __std_exception_copy(param_1 + 4,(undefined8 *)((int)this + 4));
  return this;
}


