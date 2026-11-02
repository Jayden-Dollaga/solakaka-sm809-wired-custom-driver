// Program: SM809 mouse Software.exe
// Function: __ArrayUnwind
// Entry: 004201ee
// Body: 004201ee - 00420260
// Signature: void __ArrayUnwind(void * param_1, uint param_2, uint param_3, _func_void_void_ptr * param_4)


/* WARNING: Function: __SEH_prolog4 replaced with injection: SEH_prolog4 */
/* Library Function - Single Match
    void __stdcall __ArrayUnwind(void *,unsigned int,unsigned int,void (__thiscall*)(void *))
   
   Library: Visual Studio 2019 Release */

void __ArrayUnwind(void *param_1,uint param_2,uint param_3,_func_void_void_ptr *param_4)

{
  uint uVar1;
  void *in_stack_ffffffc4;
  void *local_14;
  
  uVar1 = 0;
  while( true ) {
    if (uVar1 == param_3) break;
    guard_check_icall();
    (*param_4)(in_stack_ffffffc4);
    uVar1 = uVar1 + 1;
  }
  ExceptionList = local_14;
  return;
}


