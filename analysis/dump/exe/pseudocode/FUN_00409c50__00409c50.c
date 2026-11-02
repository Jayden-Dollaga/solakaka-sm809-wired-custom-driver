// Program: SM809 mouse Software.exe
// Function: FUN_00409c50
// Entry: 00409c50
// Body: 00409c50 - 00409c9f
// Signature: WindowImplBase * FUN_00409c50(void * this, byte param_1)


WindowImplBase * __thiscall FUN_00409c50(void *this,byte param_1)

{
  *(undefined ***)this = CFireClickWnd::vftable;
  *(undefined ***)((int)this + 0x10) = CFireClickWnd::vftable;
  *(undefined ***)((int)this + 0x20) = CFireClickWnd::vftable;
  *(undefined ***)((int)this + 0x24) = CFireClickWnd::vftable;
  *(undefined ***)((int)this + 0x28) = CFireClickWnd::vftable;
  *(undefined ***)((int)this + 0x2c) = CFireClickWnd::vftable;
  DuiLib::WindowImplBase::~WindowImplBase(this);
  if ((param_1 & 1) != 0) {
    FUN_0041feb7(this);
  }
  return this;
}


