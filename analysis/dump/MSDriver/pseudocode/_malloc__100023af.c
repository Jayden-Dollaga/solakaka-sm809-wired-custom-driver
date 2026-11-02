// Program: MSDriver.dll
// Function: _malloc
// Entry: 100023af
// Body: 100023af - 100023c0
// Signature: void * _malloc(size_t _Size)


/* Library Function - Single Match
    _malloc
   
   Library: Visual Studio 2003 Release */

void * __cdecl _malloc(size_t _Size)

{
  void *pvVar1;
  
  pvVar1 = __nh_malloc(_Size,DAT_10009f74);
  return pvVar1;
}


