// Program: SM809 mouse Software.exe
// Function: Unwind@00422c90
// Entry: 00422c90
// Body: 00422c90 - 00422c98
// Signature: undefined Unwind@00422c90(void)


void Unwind_00422c90(void)

{
  int unaff_EBP;
  
                    /* WARNING: Could not recover jumptable at 0x00422c93. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  DuiLib::WindowImplBase::~WindowImplBase(*(WindowImplBase **)(unaff_EBP + -0x10));
  return;
}


