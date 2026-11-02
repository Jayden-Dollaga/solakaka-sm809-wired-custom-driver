// Program: SM809 mouse Software.exe
// Function: FUN_0041def0
// Entry: 0041def0
// Body: 0041def0 - 0041df3c
// Signature: undefined FUN_0041def0(WindowImplBase * param_1)


void __fastcall FUN_0041def0(WindowImplBase *param_1)

{
  *(undefined ***)param_1 = CSelectGunWnd::vftable;
  *(undefined ***)(param_1 + 0x10) = CSelectGunWnd::vftable;
  *(undefined ***)(param_1 + 0x20) = CSelectGunWnd::vftable;
  *(undefined ***)(param_1 + 0x24) = CSelectGunWnd::vftable;
  *(undefined ***)(param_1 + 0x28) = CSelectGunWnd::vftable;
  *(undefined ***)(param_1 + 0x2c) = CSelectGunWnd::vftable;
  DuiLib::CStdPtrArray::~CStdPtrArray((CStdPtrArray *)(param_1 + 0x79c));
  DuiLib::CStdPtrArray::~CStdPtrArray((CStdPtrArray *)(param_1 + 0x790));
                    /* WARNING: Could not recover jumptable at 0x0041df37. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  DuiLib::WindowImplBase::~WindowImplBase(param_1);
  return;
}


