// Program: SM809 mouse Software.exe
// Function: Unwind@00423750
// Entry: 00423750
// Body: 00423750 - 00423758
// Signature: undefined Unwind@00423750(void)


void Unwind_00423750(void)

{
  int unaff_EBP;
  
                    /* WARNING: Could not recover jumptable at 0x00423753. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  DuiLib::WindowImplBase::~WindowImplBase(*(WindowImplBase **)(unaff_EBP + -0x10));
  return;
}


