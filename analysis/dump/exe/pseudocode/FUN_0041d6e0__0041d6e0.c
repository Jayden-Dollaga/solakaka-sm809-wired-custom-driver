// Program: SM809 mouse Software.exe
// Function: FUN_0041d6e0
// Entry: 0041d6e0
// Body: 0041d6e0 - 0041d70e
// Signature: undefined FUN_0041d6e0(WindowImplBase * param_1)


void __fastcall FUN_0041d6e0(WindowImplBase *param_1)

{
  *(undefined ***)param_1 = CSelectColorWnd::vftable;
  *(undefined ***)(param_1 + 0x10) = CSelectColorWnd::vftable;
  *(undefined ***)(param_1 + 0x20) = CSelectColorWnd::vftable;
  *(undefined ***)(param_1 + 0x24) = CSelectColorWnd::vftable;
  *(undefined ***)(param_1 + 0x28) = CSelectColorWnd::vftable;
  *(undefined ***)(param_1 + 0x2c) = CSelectColorWnd::vftable;
                    /* WARNING: Could not recover jumptable at 0x0041d709. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  DuiLib::WindowImplBase::~WindowImplBase(param_1);
  return;
}


