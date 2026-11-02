// Program: SM809 mouse Software.exe
// Function: Unwind@00421a30
// Entry: 00421a30
// Body: 00421a30 - 00421a38
// Signature: undefined Unwind@00421a30(void)


void Unwind_00421a30(void)

{
  int unaff_EBP;
  
                    /* WARNING: Could not recover jumptable at 0x00421a33. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  DuiLib::WindowImplBase::~WindowImplBase(*(WindowImplBase **)(unaff_EBP + -0x10));
  return;
}


