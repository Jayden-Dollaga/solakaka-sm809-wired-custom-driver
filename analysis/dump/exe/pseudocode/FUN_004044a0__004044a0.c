// Program: SM809 mouse Software.exe
// Function: FUN_004044a0
// Entry: 004044a0
// Body: 004044a0 - 0040458d
// Signature: basic_streambuf<char,std::char_traits<char>_> * FUN_004044a0(void * this, char * param_1, size_t param_2, int param_3)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

basic_streambuf<char,std::char_traits<char>_> * __thiscall
FUN_004044a0(void *this,char *param_1,size_t param_2,int param_3)

{
  undefined4 uVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 local_14;
  undefined4 local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  local_8 = DAT_00432008 ^ (int)register0x00000010 - 4U;
  if ((param_1 == (char *)0x0) && (param_2 == 0 && param_3 == 0)) {
    iVar3 = 4;
  }
  else {
    iVar3 = 0;
  }
  if (*(FILE **)((int)this + 0x4c) != (FILE *)0x0) {
    iVar3 = setvbuf(*(FILE **)((int)this + 0x4c),param_1,iVar3,param_2);
    if (iVar3 == 0) {
      iVar3 = *(int *)((int)this + 0x4c);
      *(undefined1 *)((int)this + 0x48) = 1;
      *(undefined1 *)((int)this + 0x3d) = 0;
      std::basic_streambuf<char,std::char_traits<char>_>::_Init(this);
      if (iVar3 != 0) {
        local_c = 0;
        local_10 = 0;
        local_14 = 0;
        get_stream_buffer_pointers(iVar3,&local_c,&local_10,&local_14);
        *(undefined4 *)((int)this + 0xc) = local_c;
        *(undefined4 *)((int)this + 0x10) = local_c;
        *(undefined4 *)((int)this + 0x1c) = local_10;
        *(undefined4 *)((int)this + 0x20) = local_10;
        *(undefined4 *)((int)this + 0x2c) = local_14;
        *(undefined4 *)((int)this + 0x30) = local_14;
      }
      uVar2 = DAT_00432a88;
      uVar1 = DAT_00432a84;
      *(int *)((int)this + 0x4c) = iVar3;
      *(undefined4 *)((int)this + 0x40) = uVar1;
      *(undefined4 *)((int)this + 0x44) = uVar2;
      *(undefined4 *)((int)this + 0x38) = 0;
      return this;
    }
  }
  return (basic_streambuf<char,std::char_traits<char>_> *)0x0;
}


