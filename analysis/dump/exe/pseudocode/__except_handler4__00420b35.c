// Program: SM809 mouse Software.exe
// Function: __except_handler4
// Entry: 00420b35
// Body: 00420b35 - 00420b63
// Signature: undefined __except_handler4(int * param_1, undefined4 param_2, undefined4 param_3, undefined4 param_4)


/* Library Function - Single Match
    __except_handler4
   
   Library: Visual Studio 2019 Release */

void __cdecl
__except_handler4(int *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  
  iVar1 = __filter_x86_sse2_floating_point_exception_default(*param_1);
  *param_1 = iVar1;
  except_handler4_common(&DAT_00432008,__security_check_cookie,param_1,param_2,param_3,param_4);
  return;
}


