// Program: SM809 mouse Software.exe
// Function: FUN_00405960
// Entry: 00405960
// Body: 00405960 - 00405990
// Signature: undefined4 * FUN_00405960(void * this, byte param_1)


undefined4 * __thiscall FUN_00405960(void *this,byte param_1)

{
  *(undefined ***)this = std::exception::vftable;
  __std_exception_destroy((int)this + 4);
  if ((param_1 & 1) != 0) {
    FUN_0041feb7(this);
  }
  return this;
}


