// Program: SM809 mouse Software.exe
// Function: `eh_vector_destructor_iterator'
// Entry: 00420169
// Body: 00420169 - 004201d1
// Signature: void `eh_vector_destructor_iterator'(void * param_1, uint param_2, uint param_3, _func_void_void_ptr * param_4)


/* WARNING: Function: __SEH_prolog4 replaced with injection: SEH_prolog4 */
/* Library Function - Single Match
    void __stdcall `eh vector destructor iterator'(void *,unsigned int,unsigned int,void
   (__thiscall*)(void *))
   
   Libraries: Visual Studio 2017 Release, Visual Studio 2019 Release */

void _eh_vector_destructor_iterator_
               (void *param_1,uint param_2,uint param_3,_func_void_void_ptr *param_4)

{
  void *in_stack_ffffffd0;
  void *local_14;
  
  while( true ) {
    if (param_3 == 0) break;
    guard_check_icall();
    (*param_4)(in_stack_ffffffd0);
    param_3 = param_3 - 1;
  }
  FUN_004201de();
  ExceptionList = local_14;
  return;
}


