// Program: SM809 mouse Software.exe
// Function: FUN_004059a0
// Entry: 004059a0
// Body: 004059a0 - 004059d3
// Signature: undefined4 * FUN_004059a0(void * this, int param_1)


undefined4 * __thiscall FUN_004059a0(void *this,int param_1)

{
  *(undefined ***)this = std::exception::vftable;
  *(undefined8 *)((int)this + 4) = 0;
  __std_exception_copy(param_1 + 4,(undefined8 *)((int)this + 4));
  *(undefined ***)this = std::bad_cast::vftable;
  return this;
}


