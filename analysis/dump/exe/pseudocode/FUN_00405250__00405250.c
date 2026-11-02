// Program: SM809 mouse Software.exe
// Function: FUN_00405250
// Entry: 00405250
// Body: 00405250 - 0040538a
// Signature: basic_streambuf<char,std::char_traits<char>_> * FUN_00405250(void * this, wchar_t * param_1, int param_2)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

basic_streambuf<char,std::char_traits<char>_> * __thiscall
FUN_00405250(void *this,wchar_t *param_1,int param_2)

{
  undefined4 uVar1;
  bool bVar2;
  uint uVar3;
  _iobuf *p_Var4;
  locale *plVar5;
  _Facet_base *this_00;
  undefined4 *puVar6;
  int *local_24;
  undefined4 local_20;
  undefined4 local_1c;
  uint local_18;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_0042156d;
  local_10 = ExceptionList;
  uVar3 = DAT_00432008 ^ (int)register0x00000010 - 4U;
  ExceptionList = &local_10;
  if ((*(int *)((int)this + 0x4c) != 0) ||
     (local_18 = uVar3, p_Var4 = std::_Fiopen(param_1,param_2,0x40), p_Var4 == (_iobuf *)0x0)) {
    ExceptionList = local_10;
    return (basic_streambuf<char,std::char_traits<char>_> *)0x0;
  }
  *(undefined1 *)((int)this + 0x48) = 1;
  *(undefined1 *)((int)this + 0x3d) = 0;
  std::basic_streambuf<char,std::char_traits<char>_>::_Init(this);
  local_1c = 0;
  local_20 = 0;
  local_24 = (int *)0x0;
  get_stream_buffer_pointers(p_Var4,&local_1c,&local_20,&local_24,uVar3);
  uVar1 = DAT_00432a88;
  *(undefined4 *)((int)this + 0xc) = local_1c;
  *(undefined4 *)((int)this + 0x10) = local_1c;
  *(undefined4 *)((int)this + 0x1c) = local_20;
  *(undefined4 *)((int)this + 0x20) = local_20;
  *(int **)((int)this + 0x2c) = local_24;
  *(int **)((int)this + 0x30) = local_24;
  *(undefined4 *)((int)this + 0x40) = DAT_00432a84;
  *(undefined4 *)((int)this + 0x44) = uVar1;
  *(_iobuf **)((int)this + 0x4c) = p_Var4;
  *(undefined4 *)((int)this + 0x38) = 0;
  plVar5 = (locale *)std::basic_streambuf<char,std::char_traits<char>_>::getloc(this);
  local_8 = 0;
  this_00 = FUN_00405810(plVar5);
  bVar2 = std::codecvt_base::always_noconv((codecvt_base *)this_00);
  if (bVar2) {
    *(undefined4 *)((int)this + 0x38) = 0;
  }
  else {
    *(_Facet_base **)((int)this + 0x38) = this_00;
    std::basic_streambuf<char,std::char_traits<char>_>::_Init(this);
  }
  if ((local_24 != (int *)0x0) &&
     (puVar6 = (undefined4 *)(**(code **)(*local_24 + 8))(), puVar6 != (undefined4 *)0x0)) {
    (**(code **)*puVar6)(1);
  }
  ExceptionList = local_10;
  return this;
}


