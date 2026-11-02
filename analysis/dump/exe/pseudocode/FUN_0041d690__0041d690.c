// Program: SM809 mouse Software.exe
// Function: FUN_0041d690
// Entry: 0041d690
// Body: 0041d690 - 0041d6df
// Signature: WindowImplBase * FUN_0041d690(void * this, byte param_1)


WindowImplBase * __thiscall FUN_0041d690(void *this,byte param_1)

{
  *(undefined ***)this = CSelectColorWnd::vftable;
  *(undefined ***)((int)this + 0x10) = CSelectColorWnd::vftable;
  *(undefined ***)((int)this + 0x20) = CSelectColorWnd::vftable;
  *(undefined ***)((int)this + 0x24) = CSelectColorWnd::vftable;
  *(undefined ***)((int)this + 0x28) = CSelectColorWnd::vftable;
  *(undefined ***)((int)this + 0x2c) = CSelectColorWnd::vftable;
  DuiLib::WindowImplBase::~WindowImplBase(this);
  if ((param_1 & 1) != 0) {
    FUN_0041feb7(this);
  }
  return this;
}


