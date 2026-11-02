// Program: SM809 mouse Software.exe
// Function: underflow
// Entry: 00404c00
// Body: 00404c00 - 00404c3c
// Signature: int underflow(basic_filebuf<char,std::char_traits<char>_> * this)


/* Library Function - Single Match
    protected: virtual int __thiscall std::basic_filebuf<char,struct std::char_traits<char>
   >::underflow(void)
   
   Library: Visual Studio 2019 Release */

int __thiscall
std::basic_filebuf<char,std::char_traits<char>_>::underflow
          (basic_filebuf<char,std::char_traits<char>_> *this)

{
  byte *pbVar1;
  int iVar2;
  
  pbVar1 = (byte *)**(undefined4 **)(this + 0x1c);
  if ((pbVar1 != (byte *)0x0) && (pbVar1 < pbVar1 + **(int **)(this + 0x2c))) {
    return (uint)*pbVar1;
  }
  iVar2 = (**(code **)(*(int *)this + 0x1c))();
  if (iVar2 == -1) {
    return -1;
  }
  (**(code **)(*(int *)this + 0x10))(iVar2);
  return iVar2;
}


