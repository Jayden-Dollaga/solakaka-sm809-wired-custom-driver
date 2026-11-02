// Program: SM809 mouse Software.exe
// Function: FUN_0041c2f0
// Entry: 0041c2f0
// Body: 0041c2f0 - 0041c33c
// Signature: undefined FUN_0041c2f0(WindowImplBase * param_1)


void __fastcall FUN_0041c2f0(WindowImplBase *param_1)

{
  *(undefined ***)param_1 = CMsgWnd::vftable;
  *(undefined ***)(param_1 + 0x10) = CMsgWnd::vftable;
  *(undefined ***)(param_1 + 0x20) = CMsgWnd::vftable;
  *(undefined ***)(param_1 + 0x24) = CMsgWnd::vftable;
  *(undefined ***)(param_1 + 0x28) = CMsgWnd::vftable;
  *(undefined ***)(param_1 + 0x2c) = CMsgWnd::vftable;
  DuiLib::CDuiString::~CDuiString((CDuiString *)(param_1 + 0x800));
  DuiLib::CDuiString::~CDuiString((CDuiString *)(param_1 + 0x77c));
                    /* WARNING: Could not recover jumptable at 0x0041c337. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  DuiLib::WindowImplBase::~WindowImplBase(param_1);
  return;
}


