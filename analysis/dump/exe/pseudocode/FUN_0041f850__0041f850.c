// Program: SM809 mouse Software.exe
// Function: FUN_0041f850
// Entry: 0041f850
// Body: 0041f850 - 0041f936
// Signature: undefined FUN_0041f850(void * this, CDuiString * param_1)


void __thiscall FUN_0041f850(void *this,CDuiString *param_1)

{
  bool bVar1;
  int iVar2;
  undefined4 *puVar3;
  
  bVar1 = DuiLib::CDuiString::operator==(param_1,L"click");
  if (bVar1) {
    (**(code **)(*(int *)((int)this + -0x20) + 0x20))(param_1);
    return;
  }
  bVar1 = DuiLib::CDuiString::operator==(param_1,L"checkclick");
  if (bVar1) {
    iVar2 = 0;
    puVar3 = (undefined4 *)((int)this + 0x768);
    do {
      if (*(CCheckBoxUI **)(param_1 + 0x108) == (CCheckBoxUI *)*puVar3) {
        bVar1 = DuiLib::CCheckBoxUI::GetCheck((CCheckBoxUI *)*puVar3);
        *(bool *)((int)this + iVar2 + 0x784) = bVar1;
      }
      iVar2 = iVar2 + 1;
      puVar3 = puVar3 + 1;
    } while (iVar2 < 4);
    return;
  }
  bVar1 = DuiLib::CDuiString::operator==(param_1,L"setfocus");
  if (bVar1) {
    if (*(int *)(param_1 + 0x108) == *(int *)((int)this + 0x778)) {
      (**(code **)((int)this + 0x750))(*(undefined4 *)((int)this + -0x1c));
      (**(code **)((int)this + 0x758))(1);
      return;
    }
  }
  else {
    bVar1 = DuiLib::CDuiString::operator==(param_1,L"killfocus");
    if ((bVar1) && (*(int *)(param_1 + 0x108) == *(int *)((int)this + 0x778))) {
      (**(code **)((int)this + 0x754))();
      (**(code **)((int)this + 0x758))(0);
    }
  }
  return;
}


