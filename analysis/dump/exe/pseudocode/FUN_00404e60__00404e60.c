// Program: SM809 mouse Software.exe
// Function: FUN_00404e60
// Entry: 00404e60
// Body: 00404e60 - 00404ed5
// Signature: undefined FUN_00404e60(basic_streambuf<char,std::char_traits<char>_> * param_1)


void __fastcall FUN_00404e60(basic_streambuf<char,std::char_traits<char>_> *param_1)

{
  int iVar1;
  int iVar2;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 uStack_8;
  
  uStack_8 = 0xffffffff;
  puStack_c = &LAB_004214c0;
  local_10 = ExceptionList;
  ExceptionList = &local_10;
  *(undefined ***)param_1 = std::basic_filebuf<char,std::char_traits<char>_>::vftable;
  if ((*(int *)(param_1 + 0x4c) != 0) &&
     ((basic_streambuf<char,std::char_traits<char>_> *)**(int **)(param_1 + 0xc) == param_1 + 0x3c))
  {
    iVar1 = *(int *)(param_1 + 0x54);
    iVar2 = *(int *)(param_1 + 0x50);
    **(int **)(param_1 + 0xc) = iVar2;
    **(int **)(param_1 + 0x1c) = iVar2;
    **(int **)(param_1 + 0x2c) = iVar1 - iVar2;
  }
  if (param_1[0x48] != (basic_streambuf<char,std::char_traits<char>_>)0x0) {
    FUN_004051d0(param_1);
  }
  std::basic_streambuf<char,std::char_traits<char>_>::~basic_streambuf<char,std::char_traits<char>_>
            (param_1);
  ExceptionList = local_10;
  return;
}


