// Program: SM809 mouse Software.exe
// Function: FUN_0041c410
// Entry: 0041c410
// Body: 0041c410 - 0041c46a
// Signature: undefined FUN_0041c410(void * this, CDuiString * param_1)


void __thiscall FUN_0041c410(void *this,CDuiString *param_1)

{
  int iVar1;
  bool bVar2;
  
  bVar2 = DuiLib::CDuiString::operator==(param_1,L"click");
  if (bVar2) {
    iVar1 = *(int *)(param_1 + 0x108);
    if (iVar1 == *(int *)((int)this + 0x744)) {
      DuiLib::CWindowWnd::Close((CWindowWnd *)((int)this + -0x20),1);
      return;
    }
    if ((iVar1 == *(int *)((int)this + 0x748)) || (iVar1 == *(int *)((int)this + 0x74c))) {
      DuiLib::CWindowWnd::Close((CWindowWnd *)((int)this + -0x20),0);
    }
  }
  return;
}


