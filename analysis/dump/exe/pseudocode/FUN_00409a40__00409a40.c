// Program: SM809 mouse Software.exe
// Function: FUN_00409a40
// Entry: 00409a40
// Body: 00409a40 - 00409ab9
// Signature: WindowImplBase * FUN_00409a40(void * this, byte param_1)


WindowImplBase * __thiscall FUN_00409a40(void *this,byte param_1)

{
  *(undefined ***)this = CEditMacroName::vftable;
  *(undefined ***)((int)this + 0x10) = CEditMacroName::vftable;
  *(undefined ***)((int)this + 0x20) = CEditMacroName::vftable;
  *(undefined ***)((int)this + 0x24) = CEditMacroName::vftable;
  *(undefined ***)((int)this + 0x28) = CEditMacroName::vftable;
  *(undefined ***)((int)this + 0x2c) = CEditMacroName::vftable;
  DuiLib::CDuiString::~CDuiString((CDuiString *)((int)this + 0x8f8));
  DuiLib::CDuiString::~CDuiString((CDuiString *)((int)this + 0x874));
  DuiLib::CDuiString::~CDuiString((CDuiString *)((int)this + 0x7ec));
  DuiLib::CDuiString::~CDuiString((CDuiString *)((int)this + 0x768));
  DuiLib::WindowImplBase::~WindowImplBase(this);
  if ((param_1 & 1) != 0) {
    FUN_0041feb7(this);
  }
  return this;
}


