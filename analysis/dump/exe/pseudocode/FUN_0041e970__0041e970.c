// Program: SM809 mouse Software.exe
// Function: FUN_0041e970
// Entry: 0041e970
// Body: 0041e970 - 0041e9bc
// Signature: undefined FUN_0041e970(WindowImplBase * param_1)


void __fastcall FUN_0041e970(WindowImplBase *param_1)

{
  *(undefined ***)param_1 = CSelectMacroWnd::vftable;
  *(undefined ***)(param_1 + 0x10) = CSelectMacroWnd::vftable;
  *(undefined ***)(param_1 + 0x20) = CSelectMacroWnd::vftable;
  *(undefined ***)(param_1 + 0x24) = CSelectMacroWnd::vftable;
  *(undefined ***)(param_1 + 0x28) = CSelectMacroWnd::vftable;
  *(undefined ***)(param_1 + 0x2c) = CSelectMacroWnd::vftable;
  DuiLib::CStdPtrArray::~CStdPtrArray((CStdPtrArray *)(param_1 + 0x7a4));
  DuiLib::CStdPtrArray::~CStdPtrArray((CStdPtrArray *)(param_1 + 0x798));
                    /* WARNING: Could not recover jumptable at 0x0041e9b7. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  DuiLib::WindowImplBase::~WindowImplBase(param_1);
  return;
}


