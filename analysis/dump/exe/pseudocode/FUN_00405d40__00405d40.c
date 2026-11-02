// Program: SM809 mouse Software.exe
// Function: FUN_00405d40
// Entry: 00405d40
// Body: 00405d40 - 00405d73
// Signature: undefined4 * FUN_00405d40(void * this, int param_1)


undefined4 * __thiscall FUN_00405d40(void *this,int param_1)

{
  *(undefined ***)this = std::exception::vftable;
  *(undefined8 *)((int)this + 4) = 0;
  __std_exception_copy(param_1 + 4,(undefined8 *)((int)this + 4));
  *(undefined ***)this = std::bad_alloc::vftable;
  return this;
}


