// Program: SM809 mouse Software.exe
// Function: Unwind@00421380
// Entry: 00421380
// Body: 00421380 - 00421399
// Signature: undefined Unwind@00421380(void)


void Unwind_00421380(void)

{
  int unaff_EBP;
  
  if ((*(uint *)(unaff_EBP + -0x10) & 1) == 0) {
    return;
  }
  *(uint *)(unaff_EBP + -0x10) = *(uint *)(unaff_EBP + -0x10) & 0xfffffffe;
                    /* WARNING: Could not recover jumptable at 0x00421393. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  DuiLib::CDuiString::~CDuiString(*(CDuiString **)(unaff_EBP + -0x14));
  return;
}


