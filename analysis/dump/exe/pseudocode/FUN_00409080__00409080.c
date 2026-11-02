// Program: SM809 mouse Software.exe
// Function: FUN_00409080
// Entry: 00409080
// Body: 00409080 - 004090a5
// Signature: undefined FUN_00409080(void * this, HWND__ * param_1)


void __thiscall FUN_00409080(void *this,HWND__ *param_1)

{
  if (*(char *)((int)this + 0x764) != '\0') {
    DuiLib::WindowImplBase::OnFinalMessage(this,param_1);
    (**(code **)(*(int *)this + 0x14))(1);
  }
  return;
}


