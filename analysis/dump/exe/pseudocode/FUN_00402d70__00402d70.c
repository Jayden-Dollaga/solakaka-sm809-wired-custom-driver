// Program: SM809 mouse Software.exe
// Function: FUN_00402d70
// Entry: 00402d70
// Body: 00402d70 - 00402e1d
// Signature: undefined FUN_00402d70(int * param_1)


void __fastcall FUN_00402d70(int *param_1)

{
  basic_ios<char,std::char_traits<char>_> *this;
  int iVar1;
  int iVar2;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  puStack_c = &LAB_00421060;
  local_10 = ExceptionList;
  ExceptionList = &local_10;
  this = (basic_ios<char,std::char_traits<char>_> *)(param_1 + 0x1a);
  *(undefined ***)(this + *(int *)(*param_1 + 4) + -0x68) =
       std::basic_ofstream<char,std::char_traits<char>_>::vftable;
  *(int *)(this + *(int *)(*param_1 + 4) + -0x6c) = *(int *)(*param_1 + 4) + -0x68;
  local_8 = 0;
  param_1[1] = (int)std::basic_filebuf<char,std::char_traits<char>_>::vftable;
  if ((param_1[0x14] != 0) && (*(int **)param_1[4] == param_1 + 0x10)) {
    iVar1 = param_1[0x16];
    iVar2 = param_1[0x15];
    *(int *)param_1[4] = iVar2;
    *(int *)param_1[8] = iVar2;
    *(int *)param_1[0xc] = iVar1 - iVar2;
  }
  if ((char)param_1[0x13] != '\0') {
    FUN_004051d0((basic_streambuf<char,std::char_traits<char>_> *)(param_1 + 1));
  }
  std::basic_streambuf<char,std::char_traits<char>_>::~basic_streambuf<char,std::char_traits<char>_>
            ((basic_streambuf<char,std::char_traits<char>_> *)(param_1 + 1));
  std::basic_ostream<char,std::char_traits<char>_>::~basic_ostream<char,std::char_traits<char>_>
            ((basic_ostream<char,std::char_traits<char>_> *)(param_1 + 2));
  std::basic_ios<char,std::char_traits<char>_>::~basic_ios<char,std::char_traits<char>_>(this);
  ExceptionList = local_10;
  return;
}


