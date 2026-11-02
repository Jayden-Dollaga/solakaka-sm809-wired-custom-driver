// Program: SM809 mouse Software.exe
// Function: FUN_0041f4a0
// Entry: 0041f4a0
// Body: 0041f4a0 - 0041f4ef
// Signature: undefined FUN_0041f4a0(WindowImplBase * param_1)


void __fastcall FUN_0041f4a0(WindowImplBase *param_1)

{
  *(undefined ***)param_1 = CShortcutWnd::vftable;
  *(undefined ***)(param_1 + 0x10) = CShortcutWnd::vftable;
  *(undefined ***)(param_1 + 0x20) = CShortcutWnd::vftable;
  *(undefined ***)(param_1 + 0x24) = CShortcutWnd::vftable;
  *(undefined ***)(param_1 + 0x28) = CShortcutWnd::vftable;
  *(undefined ***)(param_1 + 0x2c) = CShortcutWnd::vftable;
  if (*(HMODULE *)(param_1 + 0x7a0) != (HMODULE)0x0) {
    FreeLibrary(*(HMODULE *)(param_1 + 0x7a0));
    *(undefined4 *)(param_1 + 0x7a0) = 0;
  }
                    /* WARNING: Could not recover jumptable at 0x0041f4ea. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  DuiLib::WindowImplBase::~WindowImplBase(param_1);
  return;
}


