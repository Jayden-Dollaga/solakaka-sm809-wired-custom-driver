// Program: SM809 mouse Software.exe
// Function: FUN_00409ca0
// Entry: 00409ca0
// Body: 00409ca0 - 00409cce
// Signature: undefined FUN_00409ca0(WindowImplBase * param_1)


void __fastcall FUN_00409ca0(WindowImplBase *param_1)

{
  *(undefined ***)param_1 = CFireClickWnd::vftable;
  *(undefined ***)(param_1 + 0x10) = CFireClickWnd::vftable;
  *(undefined ***)(param_1 + 0x20) = CFireClickWnd::vftable;
  *(undefined ***)(param_1 + 0x24) = CFireClickWnd::vftable;
  *(undefined ***)(param_1 + 0x28) = CFireClickWnd::vftable;
  *(undefined ***)(param_1 + 0x2c) = CFireClickWnd::vftable;
                    /* WARNING: Could not recover jumptable at 0x00409cc9. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  DuiLib::WindowImplBase::~WindowImplBase(param_1);
  return;
}


