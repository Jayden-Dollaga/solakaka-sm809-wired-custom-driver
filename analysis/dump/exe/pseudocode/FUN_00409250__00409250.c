// Program: SM809 mouse Software.exe
// Function: FUN_00409250
// Entry: 00409250
// Body: 00409250 - 004092c9
// Signature: WindowImplBase * FUN_00409250(void * this, byte param_1)


WindowImplBase * __thiscall FUN_00409250(void *this,byte param_1)

{
  *(undefined ***)this = CEditGunName::vftable;
  *(undefined ***)((int)this + 0x10) = CEditGunName::vftable;
  *(undefined ***)((int)this + 0x20) = CEditGunName::vftable;
  *(undefined ***)((int)this + 0x24) = CEditGunName::vftable;
  *(undefined ***)((int)this + 0x28) = CEditGunName::vftable;
  *(undefined ***)((int)this + 0x2c) = CEditGunName::vftable;
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


