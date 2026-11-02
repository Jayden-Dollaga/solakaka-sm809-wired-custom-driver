// Program: SM809 mouse Software.exe
// Function: FUN_00404ee0
// Entry: 00404ee0
// Body: 00404ee0 - 00404fe2
// Signature: basic_ostream<char,std::char_traits<char>_> * FUN_00404ee0(void * this, wchar_t * param_1)


basic_ostream<char,std::char_traits<char>_> * __thiscall FUN_00404ee0(void *this,wchar_t *param_1)

{
  undefined4 uVar1;
  undefined4 uVar2;
  basic_streambuf<char,std::char_traits<char>_> *pbVar3;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00421522;
  local_10 = ExceptionList;
  ExceptionList = &local_10;
  *(undefined ***)this = &PTR_00425094;
  std::basic_ios<char,std::char_traits<char>_>::basic_ios<char,std::char_traits<char>_>
            ((basic_ios<char,std::char_traits<char>_> *)((int)this + 0x68));
  pbVar3 = (basic_streambuf<char,std::char_traits<char>_> *)((int)this + 4);
  local_8 = 0;
  std::basic_ostream<char,std::char_traits<char>_>::basic_ostream<char,std::char_traits<char>_>
            (this,pbVar3,false);
  local_8 = 1;
  *(undefined ***)((int)this + *(int *)(*(int *)this + 4)) =
       std::basic_ofstream<char,std::char_traits<char>_>::vftable;
  *(int *)(*(int *)(*(int *)this + 4) + -4 + (int)this) = *(int *)(*(int *)this + 4) + -0x68;
  std::basic_streambuf<char,std::char_traits<char>_>::basic_streambuf<char,std::char_traits<char>_>
            (pbVar3);
  local_8._0_1_ = 2;
  *(undefined ***)pbVar3 = std::basic_filebuf<char,std::char_traits<char>_>::vftable;
  *(undefined1 *)((int)this + 0x4c) = 0;
  *(undefined1 *)((int)this + 0x41) = 0;
  std::basic_streambuf<char,std::char_traits<char>_>::_Init(pbVar3);
  uVar2 = DAT_00432a88;
  uVar1 = DAT_00432a84;
  *(undefined4 *)((int)this + 0x50) = 0;
  *(undefined4 *)((int)this + 0x44) = uVar1;
  *(undefined4 *)((int)this + 0x48) = uVar2;
  *(undefined4 *)((int)this + 0x3c) = 0;
  local_8 = CONCAT31(local_8._1_3_,3);
  pbVar3 = FUN_00405250(pbVar3,param_1,0x22);
  if (pbVar3 == (basic_streambuf<char,std::char_traits<char>_> *)0x0) {
    std::basic_ios<char,std::char_traits<char>_>::setstate
              ((basic_ios<char,std::char_traits<char>_> *)(*(int *)(*(int *)this + 4) + (int)this),2
               ,false);
  }
  ExceptionList = local_10;
  return this;
}


