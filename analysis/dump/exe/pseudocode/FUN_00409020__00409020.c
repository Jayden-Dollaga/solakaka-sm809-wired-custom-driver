// Program: SM809 mouse Software.exe
// Function: FUN_00409020
// Entry: 00409020
// Body: 00409020 - 0040907d
// Signature: WindowImplBase * FUN_00409020(void * this, byte param_1)


WindowImplBase * __thiscall FUN_00409020(void *this,byte param_1)

{
  *(undefined ***)this = CDPIMsg::vftable;
  *(undefined ***)((int)this + 0x10) = CDPIMsg::vftable;
  *(undefined ***)((int)this + 0x20) = CDPIMsg::vftable;
  *(undefined ***)((int)this + 0x24) = CDPIMsg::vftable;
  *(undefined ***)((int)this + 0x28) = CDPIMsg::vftable;
  *(undefined ***)((int)this + 0x2c) = CDPIMsg::vftable;
  DuiLib::CDuiString::~CDuiString((CDuiString *)((int)this + 0x76c));
  DuiLib::WindowImplBase::~WindowImplBase(this);
  if ((param_1 & 1) != 0) {
    FUN_0041feb7(this);
  }
  return this;
}


