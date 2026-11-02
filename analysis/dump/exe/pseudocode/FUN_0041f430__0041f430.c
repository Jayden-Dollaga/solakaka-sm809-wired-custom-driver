// Program: SM809 mouse Software.exe
// Function: FUN_0041f430
// Entry: 0041f430
// Body: 0041f430 - 0041f49c
// Signature: WindowImplBase * FUN_0041f430(void * this, byte param_1)


WindowImplBase * __thiscall FUN_0041f430(void *this,byte param_1)

{
  *(undefined ***)this = CShortcutWnd::vftable;
  *(undefined ***)((int)this + 0x10) = CShortcutWnd::vftable;
  *(undefined ***)((int)this + 0x20) = CShortcutWnd::vftable;
  *(undefined ***)((int)this + 0x24) = CShortcutWnd::vftable;
  *(undefined ***)((int)this + 0x28) = CShortcutWnd::vftable;
  *(undefined ***)((int)this + 0x2c) = CShortcutWnd::vftable;
  if (*(HMODULE *)((int)this + 0x7a0) != (HMODULE)0x0) {
    FreeLibrary(*(HMODULE *)((int)this + 0x7a0));
    *(undefined4 *)((int)this + 0x7a0) = 0;
  }
  DuiLib::WindowImplBase::~WindowImplBase(this);
  if ((param_1 & 1) != 0) {
    FUN_0041feb7(this);
  }
  return this;
}


