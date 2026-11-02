// Program: SM809 mouse Software.exe
// Function: __onexit
// Entry: 00420127
// Body: 00420127 - 00420153
// Signature: _onexit_t __onexit(_onexit_t _Func)


/* Library Function - Single Match
    __onexit
   
   Library: Visual Studio 2019 Release */

_onexit_t __cdecl __onexit(_onexit_t _Func)

{
  int iVar1;
  
  if (DAT_00432724 == -1) {
    iVar1 = crt_atexit();
  }
  else {
    iVar1 = register_onexit_function(&DAT_00432724,_Func);
  }
  return (_onexit_t)(~-(uint)(iVar1 != 0) & (uint)_Func);
}


