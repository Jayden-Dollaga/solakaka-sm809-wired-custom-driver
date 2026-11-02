// Program: SM809 mouse Software.exe
// Function: FUN_0041e9c0
// Entry: 0041e9c0
// Body: 0041e9c0 - 0041e9e5
// Signature: undefined FUN_0041e9c0(void * this, HWND__ * param_1)


void __thiscall FUN_0041e9c0(void *this,HWND__ *param_1)

{
  if (*(char *)((int)this + 0x7c0) != '\0') {
    DuiLib::WindowImplBase::OnFinalMessage(this,param_1);
    (**(code **)(*(int *)this + 0x14))(1);
  }
  return;
}


