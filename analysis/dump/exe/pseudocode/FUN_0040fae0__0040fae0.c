// Program: SM809 mouse Software.exe
// Function: FUN_0040fae0
// Entry: 0040fae0
// Body: 0040fae0 - 0040fb28
// Signature: undefined FUN_0040fae0(void * this, int param_1)


void __thiscall FUN_0040fae0(void *this,int param_1)

{
  if (*(int *)(param_1 + 0x118) == 3) {
    DuiLib::CPaintManagerUI::KillTimer
              (*(CPaintManagerUI **)((int)this + 0x10),*(CControlUI **)((int)this + 0x360),3);
    if ((*(CListUI **)((int)this + 0x360) != (CListUI *)0x0) && (0 < *(int *)((int)this + 0x2b4))) {
                    /* WARNING: Could not recover jumptable at 0x0040fb1e. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      DuiLib::CListUI::EnsureVisible
                (*(CListUI **)((int)this + 0x360),*(int *)((int)this + 0x2b4) + -1);
      return;
    }
  }
  return;
}


