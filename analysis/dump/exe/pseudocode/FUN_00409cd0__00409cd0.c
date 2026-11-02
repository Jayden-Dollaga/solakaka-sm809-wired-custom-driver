// Program: SM809 mouse Software.exe
// Function: FUN_00409cd0
// Entry: 00409cd0
// Body: 00409cd0 - 00409cf5
// Signature: undefined FUN_00409cd0(void * this, HWND__ * param_1)


void __thiscall FUN_00409cd0(void *this,HWND__ *param_1)

{
  if (*(char *)((int)this + 0x778) != '\0') {
    DuiLib::WindowImplBase::OnFinalMessage(this,param_1);
    (**(code **)(*(int *)this + 0x14))(1);
  }
  return;
}


