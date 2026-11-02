// Program: SM809 mouse Software.exe
// Function: FUN_00404320
// Entry: 00404320
// Body: 00404320 - 00404422
// Signature: basic_istream<char,std::char_traits<char>_> * FUN_00404320(void * this, wchar_t * param_1)


basic_istream<char,std::char_traits<char>_> * __thiscall FUN_00404320(void *this,wchar_t *param_1)

{
  undefined4 uVar1;
  undefined4 uVar2;
  basic_streambuf<char,std::char_traits<char>_> *pbVar3;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00421462;
  local_10 = ExceptionList;
  ExceptionList = &local_10;
  *(undefined ***)this = &PTR_004250e4;
  std::basic_ios<char,std::char_traits<char>_>::basic_ios<char,std::char_traits<char>_>
            ((basic_ios<char,std::char_traits<char>_> *)((int)this + 0x70));
  pbVar3 = (basic_streambuf<char,std::char_traits<char>_> *)((int)this + 0x10);
  local_8 = 0;
  std::basic_istream<char,std::char_traits<char>_>::basic_istream<char,std::char_traits<char>_>
            (this,pbVar3,false);
  local_8 = 1;
  *(undefined ***)((int)this + *(int *)(*(int *)this + 4)) =
       std::basic_ifstream<char,std::char_traits<char>_>::vftable;
  *(int *)(*(int *)(*(int *)this + 4) + -4 + (int)this) = *(int *)(*(int *)this + 4) + -0x70;
  std::basic_streambuf<char,std::char_traits<char>_>::basic_streambuf<char,std::char_traits<char>_>
            (pbVar3);
  local_8._0_1_ = 2;
  *(undefined ***)pbVar3 = std::basic_filebuf<char,std::char_traits<char>_>::vftable;
  *(undefined1 *)((int)this + 0x58) = 0;
  *(undefined1 *)((int)this + 0x4d) = 0;
  std::basic_streambuf<char,std::char_traits<char>_>::_Init(pbVar3);
  uVar2 = DAT_00432a88;
  uVar1 = DAT_00432a84;
  *(undefined4 *)((int)this + 0x5c) = 0;
  *(undefined4 *)((int)this + 0x50) = uVar1;
  *(undefined4 *)((int)this + 0x54) = uVar2;
  *(undefined4 *)((int)this + 0x48) = 0;
  local_8 = CONCAT31(local_8._1_3_,3);
  pbVar3 = FUN_00405250(pbVar3,param_1,0x21);
  if (pbVar3 == (basic_streambuf<char,std::char_traits<char>_> *)0x0) {
    std::basic_ios<char,std::char_traits<char>_>::setstate
              ((basic_ios<char,std::char_traits<char>_> *)(*(int *)(*(int *)this + 4) + (int)this),2
               ,false);
  }
  ExceptionList = local_10;
  return this;
}


