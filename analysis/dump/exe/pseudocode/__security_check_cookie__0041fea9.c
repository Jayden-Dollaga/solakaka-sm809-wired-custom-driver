// Program: SM809 mouse Software.exe
// Function: __security_check_cookie
// Entry: 0041fea9
// Body: 0041fea9 - 0041feb6
// Signature: void __security_check_cookie(uintptr_t _StackCookie)


/* WARNING: This is an inlined function */

void __fastcall __security_check_cookie(uintptr_t _StackCookie)

{
  undefined1 in_stack_00000004;
  
  if (_StackCookie == DAT_00432008) {
    return;
  }
  FUN_004202a6(in_stack_00000004);
  return;
}


