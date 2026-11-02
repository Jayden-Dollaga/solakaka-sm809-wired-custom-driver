// Program: SM809 mouse Software.exe
// Function: FUN_0041c280
// Entry: 0041c280
// Body: 0041c280 - 0041c2e9
// Signature: WindowImplBase * FUN_0041c280(void * this, byte param_1)


WindowImplBase * __thiscall FUN_0041c280(void *this,byte param_1)

{
  *(undefined ***)this = CMsgWnd::vftable;
  *(undefined ***)((int)this + 0x10) = CMsgWnd::vftable;
  *(undefined ***)((int)this + 0x20) = CMsgWnd::vftable;
  *(undefined ***)((int)this + 0x24) = CMsgWnd::vftable;
  *(undefined ***)((int)this + 0x28) = CMsgWnd::vftable;
  *(undefined ***)((int)this + 0x2c) = CMsgWnd::vftable;
  DuiLib::CDuiString::~CDuiString((CDuiString *)((int)this + 0x800));
  DuiLib::CDuiString::~CDuiString((CDuiString *)((int)this + 0x77c));
  DuiLib::WindowImplBase::~WindowImplBase(this);
  if ((param_1 & 1) != 0) {
    FUN_0041feb7(this);
  }
  return this;
}


