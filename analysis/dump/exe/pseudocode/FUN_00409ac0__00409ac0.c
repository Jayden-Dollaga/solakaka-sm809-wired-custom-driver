// Program: SM809 mouse Software.exe
// Function: FUN_00409ac0
// Entry: 00409ac0
// Body: 00409ac0 - 00409b1c
// Signature: undefined FUN_00409ac0(WindowImplBase * param_1)


void __fastcall FUN_00409ac0(WindowImplBase *param_1)

{
  *(undefined ***)param_1 = CEditMacroName::vftable;
  *(undefined ***)(param_1 + 0x10) = CEditMacroName::vftable;
  *(undefined ***)(param_1 + 0x20) = CEditMacroName::vftable;
  *(undefined ***)(param_1 + 0x24) = CEditMacroName::vftable;
  *(undefined ***)(param_1 + 0x28) = CEditMacroName::vftable;
  *(undefined ***)(param_1 + 0x2c) = CEditMacroName::vftable;
  DuiLib::CDuiString::~CDuiString((CDuiString *)(param_1 + 0x8f8));
  DuiLib::CDuiString::~CDuiString((CDuiString *)(param_1 + 0x874));
  DuiLib::CDuiString::~CDuiString((CDuiString *)(param_1 + 0x7ec));
  DuiLib::CDuiString::~CDuiString((CDuiString *)(param_1 + 0x768));
                    /* WARNING: Could not recover jumptable at 0x00409b17. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  DuiLib::WindowImplBase::~WindowImplBase(param_1);
  return;
}


