// Program: SM809 mouse Software.exe
// Function: FUN_0041df40
// Entry: 0041df40
// Body: 0041df40 - 0041df65
// Signature: undefined FUN_0041df40(void * this, HWND__ * param_1)


void __thiscall FUN_0041df40(void *this,HWND__ *param_1)

{
  if (*(char *)((int)this + 0x7b0) != '\0') {
    DuiLib::WindowImplBase::OnFinalMessage(this,param_1);
    (**(code **)(*(int *)this + 0x14))(1);
  }
  return;
}


