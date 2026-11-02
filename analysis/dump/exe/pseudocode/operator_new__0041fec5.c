// Program: SM809 mouse Software.exe
// Function: operator_new
// Entry: 0041fec5
// Body: 0041fec5 - 0041fef4
// Signature: void * operator_new(uint param_1)


/* Library Function - Single Match
    void * __cdecl operator new(unsigned int)
   
   Libraries: Visual Studio 2017 Release, Visual Studio 2019 Release */

void * __cdecl operator_new(uint param_1)

{
  int iVar1;
  void *pvVar2;
  undefined4 auStack_14 [2];
  undefined4 uStack_c;
  
  do {
    uStack_c = 0x41fedf;
    pvVar2 = malloc(param_1);
    if (pvVar2 != (void *)0x0) {
      return pvVar2;
    }
    uStack_c = 0x41fed2;
    iVar1 = _callnewh(param_1);
  } while (iVar1 != 0);
  if (param_1 == 0xffffffff) {
    FUN_00405ce0(auStack_14);
                    /* WARNING: Subroutine does not return */
    _CxxThrowException(auStack_14,(ThrowInfo *)&DAT_0042d8fc);
  }
  pvVar2 = (void *)FUN_004206e3();
  return pvVar2;
}


