// Program: SM809 mouse Software.exe
// Function: FUN_0041d020
// Entry: 0041d020
// Body: 0041d020 - 0041d09f
// Signature: undefined FUN_0041d020(void * this, int param_1)


void __thiscall FUN_0041d020(void *this,int param_1)

{
  CCheckBoxUI *pCVar1;
  bool bVar2;
  
  pCVar1 = *(CCheckBoxUI **)(param_1 + 0x108);
  if (pCVar1 == *(CCheckBoxUI **)((int)this + 0x114)) {
    bVar2 = DuiLib::CCheckBoxUI::GetCheck(*(CCheckBoxUI **)((int)this + 0x114));
    *(uint *)(DAT_00432aa0 + 0x70) = (uint)bVar2;
  }
  else {
    if (pCVar1 == *(CCheckBoxUI **)((int)this + 0x118)) {
      bVar2 = DuiLib::CCheckBoxUI::GetCheck(*(CCheckBoxUI **)((int)this + 0x118));
      *(uint *)(DAT_00432aa0 + 0x74) = (uint)bVar2;
      return;
    }
    if (pCVar1 == *(CCheckBoxUI **)((int)this + 0x124)) {
      bVar2 = DuiLib::CCheckBoxUI::GetCheck(*(CCheckBoxUI **)((int)this + 0x124));
      *(uint *)(DAT_00432aa0 + 0x134) = (uint)bVar2;
                    /* WARNING: Could not recover jumptable at 0x0041d09a. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(**(int **)((int)this + 0x128) + 0xf8))();
      return;
    }
  }
  return;
}


