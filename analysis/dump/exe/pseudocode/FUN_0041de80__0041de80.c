// Program: SM809 mouse Software.exe
// Function: FUN_0041de80
// Entry: 0041de80
// Body: 0041de80 - 0041dee9
// Signature: WindowImplBase * FUN_0041de80(void * this, byte param_1)


WindowImplBase * __thiscall FUN_0041de80(void *this,byte param_1)

{
  *(undefined ***)this = CSelectGunWnd::vftable;
  *(undefined ***)((int)this + 0x10) = CSelectGunWnd::vftable;
  *(undefined ***)((int)this + 0x20) = CSelectGunWnd::vftable;
  *(undefined ***)((int)this + 0x24) = CSelectGunWnd::vftable;
  *(undefined ***)((int)this + 0x28) = CSelectGunWnd::vftable;
  *(undefined ***)((int)this + 0x2c) = CSelectGunWnd::vftable;
  DuiLib::CStdPtrArray::~CStdPtrArray((CStdPtrArray *)((int)this + 0x79c));
  DuiLib::CStdPtrArray::~CStdPtrArray((CStdPtrArray *)((int)this + 0x790));
  DuiLib::WindowImplBase::~WindowImplBase(this);
  if ((param_1 & 1) != 0) {
    FUN_0041feb7(this);
  }
  return this;
}


