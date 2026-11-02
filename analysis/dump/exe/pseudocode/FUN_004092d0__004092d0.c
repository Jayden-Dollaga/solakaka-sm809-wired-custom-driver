// Program: SM809 mouse Software.exe
// Function: FUN_004092d0
// Entry: 004092d0
// Body: 004092d0 - 0040932c
// Signature: undefined FUN_004092d0(WindowImplBase * param_1)


void __fastcall FUN_004092d0(WindowImplBase *param_1)

{
  *(undefined ***)param_1 = CEditGunName::vftable;
  *(undefined ***)(param_1 + 0x10) = CEditGunName::vftable;
  *(undefined ***)(param_1 + 0x20) = CEditGunName::vftable;
  *(undefined ***)(param_1 + 0x24) = CEditGunName::vftable;
  *(undefined ***)(param_1 + 0x28) = CEditGunName::vftable;
  *(undefined ***)(param_1 + 0x2c) = CEditGunName::vftable;
  DuiLib::CDuiString::~CDuiString((CDuiString *)(param_1 + 0x8f8));
  DuiLib::CDuiString::~CDuiString((CDuiString *)(param_1 + 0x874));
  DuiLib::CDuiString::~CDuiString((CDuiString *)(param_1 + 0x7ec));
  DuiLib::CDuiString::~CDuiString((CDuiString *)(param_1 + 0x768));
                    /* WARNING: Could not recover jumptable at 0x00409327. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  DuiLib::WindowImplBase::~WindowImplBase(param_1);
  return;
}


