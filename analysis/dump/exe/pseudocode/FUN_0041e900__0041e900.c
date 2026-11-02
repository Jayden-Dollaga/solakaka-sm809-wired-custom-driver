// Program: SM809 mouse Software.exe
// Function: FUN_0041e900
// Entry: 0041e900
// Body: 0041e900 - 0041e969
// Signature: WindowImplBase * FUN_0041e900(void * this, byte param_1)


WindowImplBase * __thiscall FUN_0041e900(void *this,byte param_1)

{
  *(undefined ***)this = CSelectMacroWnd::vftable;
  *(undefined ***)((int)this + 0x10) = CSelectMacroWnd::vftable;
  *(undefined ***)((int)this + 0x20) = CSelectMacroWnd::vftable;
  *(undefined ***)((int)this + 0x24) = CSelectMacroWnd::vftable;
  *(undefined ***)((int)this + 0x28) = CSelectMacroWnd::vftable;
  *(undefined ***)((int)this + 0x2c) = CSelectMacroWnd::vftable;
  DuiLib::CStdPtrArray::~CStdPtrArray((CStdPtrArray *)((int)this + 0x7a4));
  DuiLib::CStdPtrArray::~CStdPtrArray((CStdPtrArray *)((int)this + 0x798));
  DuiLib::WindowImplBase::~WindowImplBase(this);
  if ((param_1 & 1) != 0) {
    FUN_0041feb7(this);
  }
  return this;
}


