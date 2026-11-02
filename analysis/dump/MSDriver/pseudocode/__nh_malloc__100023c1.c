// Program: MSDriver.dll
// Function: __nh_malloc
// Entry: 100023c1
// Body: 100023c1 - 100023ec
// Signature: void * __nh_malloc(size_t _Size, int _NhFlag)


/* Library Function - Single Match
    __nh_malloc
   
   Library: Visual Studio 2003 Release */

void * __cdecl __nh_malloc(size_t _Size,int _NhFlag)

{
  int *piVar1;
  int iVar2;
  
  if (_Size < 0xffffffe1) {
    do {
      piVar1 = FUN_100023ed((uint *)_Size);
      if (piVar1 != (int *)0x0) {
        return piVar1;
      }
      if (_NhFlag == 0) {
        return (void *)0x0;
      }
      iVar2 = FUN_10003098(_Size);
    } while (iVar2 != 0);
  }
  return (void *)0x0;
}


