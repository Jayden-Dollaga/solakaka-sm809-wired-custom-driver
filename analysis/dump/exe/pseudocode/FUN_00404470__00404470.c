// Program: SM809 mouse Software.exe
// Function: FUN_00404470
// Entry: 00404470
// Body: 00404470 - 0040449d
// Signature: undefined4 FUN_00404470(int * param_1)


undefined4 __fastcall FUN_00404470(int *param_1)

{
  int iVar1;
  
  if (param_1[0x13] != 0) {
    iVar1 = (**(code **)(*param_1 + 0xc))(0xffffffff);
    if (iVar1 != -1) {
      iVar1 = fflush((FILE *)param_1[0x13]);
      if (iVar1 < 0) {
        return 0xffffffff;
      }
    }
  }
  return 0;
}


