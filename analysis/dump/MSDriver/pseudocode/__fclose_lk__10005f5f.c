// Program: MSDriver.dll
// Function: __fclose_lk
// Entry: 10005f5f
// Body: 10005f5f - 10005faa
// Signature: undefined4 __fclose_lk(FILE * param_1)


/* Library Function - Single Match
    __fclose_lk
   
   Library: Visual Studio 2003 Release */

undefined4 __cdecl __fclose_lk(FILE *param_1)

{
  int iVar1;
  undefined4 uVar2;
  
  uVar2 = 0xffffffff;
  if ((param_1->_flag & 0x83) != 0) {
    uVar2 = FUN_10005a84((int *)param_1);
    __freebuf(param_1);
    iVar1 = FUN_1000638f(param_1->_file);
    if (iVar1 < 0) {
      uVar2 = 0xffffffff;
    }
    else if (param_1->_tmpfname != (char *)0x0) {
      FUN_100022da(param_1->_tmpfname);
      param_1->_tmpfname = (char *)0x0;
    }
  }
  param_1->_flag = 0;
  return uVar2;
}


