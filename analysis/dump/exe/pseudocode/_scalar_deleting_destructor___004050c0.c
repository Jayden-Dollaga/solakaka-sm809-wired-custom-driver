// Program: SM809 mouse Software.exe
// Function: `scalar_deleting_destructor'
// Entry: 004050c0
// Body: 004050c0 - 004050e8
// Signature: void * `scalar_deleting_destructor'(basic_stringstream<char,std::char_traits<char>,std::allocator<char>_> * this, uint param_1)


/* Library Function - Single Match
    public: virtual void * __thiscall std::basic_stringstream<char,struct
   std::char_traits<char>,class std::allocator<char> >::`scalar deleting destructor'(unsigned int)
   
   Library: Visual Studio 2019 Release */

void * __thiscall
std::basic_stringstream<char,std::char_traits<char>,std::allocator<char>_>::
_scalar_deleting_destructor_
          (basic_stringstream<char,std::char_traits<char>,std::allocator<char>_> *this,uint param_1)

{
  basic_stringstream<char,std::char_traits<char>,std::allocator<char>_> *pbVar1;
  
  pbVar1 = this + -0x68;
  FUN_00402d70((int *)pbVar1);
  if ((param_1 & 1) != 0) {
    FUN_0041feb7(pbVar1);
  }
  return pbVar1;
}


