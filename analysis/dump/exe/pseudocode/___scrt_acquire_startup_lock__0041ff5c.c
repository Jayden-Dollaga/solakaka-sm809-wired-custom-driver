// Program: SM809 mouse Software.exe
// Function: ___scrt_acquire_startup_lock
// Entry: 0041ff5c
// Body: 0041ff5c - 0041ff8d
// Signature: undefined4 ___scrt_acquire_startup_lock(void)


/* Library Function - Single Match
    ___scrt_acquire_startup_lock
   
   Libraries: Visual Studio 2017 Release, Visual Studio 2019 Release */

undefined4 ___scrt_acquire_startup_lock(void)

{
  bool bVar1;
  undefined3 extraout_var;
  void *pvVar2;
  
  bVar1 = ___scrt_is_ucrt_dll_in_use();
  if (CONCAT31(extraout_var,bVar1) != 0) {
    while( true ) {
      pvVar2 = (void *)0x0;
      LOCK();
      if (DAT_0043271c == (void *)0x0) {
        DAT_0043271c = StackBase;
      }
      else {
        pvVar2 = DAT_0043271c;
      }
      UNLOCK();
      if (pvVar2 == (void *)0x0) break;
      if (StackBase == pvVar2) {
        return CONCAT31((int3)((uint)pvVar2 >> 8),1);
      }
    }
  }
  return 0;
}


