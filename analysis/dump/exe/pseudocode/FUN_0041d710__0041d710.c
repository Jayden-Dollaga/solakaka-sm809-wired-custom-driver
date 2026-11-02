// Program: SM809 mouse Software.exe
// Function: FUN_0041d710
// Entry: 0041d710
// Body: 0041d710 - 0041d735
// Signature: undefined FUN_0041d710(void * this, HWND__ * param_1)


void __thiscall FUN_0041d710(void *this,HWND__ *param_1)

{
  if (*(char *)((int)this + 0x784) != '\0') {
    DuiLib::WindowImplBase::OnFinalMessage(this,param_1);
    (**(code **)(*(int *)this + 0x14))(1);
  }
  return;
}


