// Program: Hook.dll
// Function: _malloc
// Entry: 100033d5
// Body: 100033d5 - 100033e6
// Signature: void * _malloc(size_t _Size)


/* Library Function - Single Match
    _malloc
   
   Library: Visual Studio 2003 Release */

void * __cdecl _malloc(size_t _Size)

{
  void *pvVar1;
  
  pvVar1 = __nh_malloc(_Size,DAT_10007f38);
  return pvVar1;
}


