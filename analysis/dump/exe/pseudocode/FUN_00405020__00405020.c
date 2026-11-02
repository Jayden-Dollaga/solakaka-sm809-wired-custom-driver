// Program: SM809 mouse Software.exe
// Function: FUN_00405020
// Entry: 00405020
// Body: 00405020 - 004050b1
// Signature: basic_streambuf<char,std::char_traits<char>_> * FUN_00405020(void * this, byte param_1)


basic_streambuf<char,std::char_traits<char>_> * __thiscall FUN_00405020(void *this,byte param_1)

{
  int iVar1;
  int iVar2;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  puStack_c = &LAB_00421540;
  local_10 = ExceptionList;
  ExceptionList = &local_10;
  local_8 = 0;
  *(undefined ***)this = std::basic_filebuf<char,std::char_traits<char>_>::vftable;
  if ((*(int *)((int)this + 0x4c) != 0) && (**(int **)((int)this + 0xc) == (int)this + 0x3c)) {
    iVar1 = *(int *)((int)this + 0x54);
    iVar2 = *(int *)((int)this + 0x50);
    **(int **)((int)this + 0xc) = iVar2;
    **(int **)((int)this + 0x1c) = iVar2;
    **(int **)((int)this + 0x2c) = iVar1 - iVar2;
  }
  if (*(char *)((int)this + 0x48) != '\0') {
    FUN_004051d0(this);
  }
  std::basic_streambuf<char,std::char_traits<char>_>::~basic_streambuf<char,std::char_traits<char>_>
            (this);
  if ((param_1 & 1) != 0) {
    FUN_0041feb7(this);
  }
  ExceptionList = local_10;
  return this;
}


