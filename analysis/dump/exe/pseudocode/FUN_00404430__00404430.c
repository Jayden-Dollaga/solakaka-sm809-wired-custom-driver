// Program: SM809 mouse Software.exe
// Function: FUN_00404430
// Entry: 00404430
// Body: 00404430 - 0040446a
// Signature: undefined FUN_00404430(void * this, locale * param_1)


void __thiscall FUN_00404430(void *this,locale *param_1)

{
  bool bVar1;
  _Facet_base *this_00;
  
  this_00 = FUN_00405810(param_1);
  bVar1 = std::codecvt_base::always_noconv((codecvt_base *)this_00);
  if (bVar1) {
    *(undefined4 *)((int)this + 0x38) = 0;
    return;
  }
  *(_Facet_base **)((int)this + 0x38) = this_00;
  std::basic_streambuf<char,std::char_traits<char>_>::_Init(this);
  return;
}


