// Program: SM809 mouse Software.exe
// Function: FUN_00405bb0
// Entry: 00405bb0
// Body: 00405bb0 - 00405bef
// Signature: undefined4 * FUN_00405bb0(void * this, uint param_1)


undefined4 * __thiscall FUN_00405bb0(void *this,uint param_1)

{
  *(undefined ***)this = Gdiplus::Image::vftable;
  GdipDisposeImage(*(undefined4 *)((int)this + 4));
  if ((param_1 & 1) != 0) {
    if ((param_1 & 4) == 0) {
      GdipFree(this);
      return this;
    }
    guard_check_icall();
  }
  return this;
}


