// Program: SM809 mouse Software.exe
// Function: FUN_0041f4f0
// Entry: 0041f4f0
// Body: 0041f4f0 - 0041f515
// Signature: undefined FUN_0041f4f0(void * this, HWND__ * param_1)


void __thiscall FUN_0041f4f0(void *this,HWND__ *param_1)

{
  if (*(char *)((int)this + 0x79c) != '\0') {
    DuiLib::WindowImplBase::OnFinalMessage(this,param_1);
    (**(code **)(*(int *)this + 0x14))(1);
  }
  return;
}


