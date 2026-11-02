// Program: SM809 mouse Software.exe
// Function: FUN_00402e30
// Entry: 00402e30
// Body: 00402e30 - 00402edd
// Signature: undefined FUN_00402e30(int * param_1)


void __fastcall FUN_00402e30(int *param_1)

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
  this = (basic_ios<char,std::char_traits<char>_> *)(param_1 + 0x1c);
  *(undefined ***)(this + *(int *)(*param_1 + 4) + -0x70) =
       std::basic_ifstream<char,std::char_traits<char>_>::vftable;
  *(int *)(this + *(int *)(*param_1 + 4) + -0x74) = *(int *)(*param_1 + 4) + -0x70;
  local_8 = 0;
  param_1[4] = (int)std::basic_filebuf<char,std::char_traits<char>_>::vftable;
  if ((param_1[0x17] != 0) && (*(int **)param_1[7] == param_1 + 0x13)) {
    iVar1 = param_1[0x19];
    iVar2 = param_1[0x18];
    *(int *)param_1[7] = iVar2;
    *(int *)param_1[0xb] = iVar2;
    *(int *)param_1[0xf] = iVar1 - iVar2;
  }
  if ((char)param_1[0x16] != '\0') {
    FUN_004051d0((basic_streambuf<char,std::char_traits<char>_> *)(param_1 + 4));
  }
  std::basic_streambuf<char,std::char_traits<char>_>::~basic_streambuf<char,std::char_traits<char>_>
            ((basic_streambuf<char,std::char_traits<char>_> *)(param_1 + 4));
  std::basic_istream<char,std::char_traits<char>_>::~basic_istream<char,std::char_traits<char>_>
            ((basic_istream<char,std::char_traits<char>_> *)(param_1 + 6));
  std::basic_ios<char,std::char_traits<char>_>::~basic_ios<char,std::char_traits<char>_>(this);
  ExceptionList = local_10;
  return;
}


