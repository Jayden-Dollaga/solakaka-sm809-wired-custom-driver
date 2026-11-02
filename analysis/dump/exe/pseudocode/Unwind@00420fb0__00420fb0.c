// Program: SM809 mouse Software.exe
// Function: Unwind@00420fb0
// Entry: 00420fb0
// Body: 00420fb0 - 00420fc9
// Signature: undefined Unwind@00420fb0(void)


void Unwind_00420fb0(void)

{
  int unaff_EBP;
  
  if ((*(uint *)(unaff_EBP + -0x10) & 1) == 0) {
    return;
  }
  *(uint *)(unaff_EBP + -0x10) = *(uint *)(unaff_EBP + -0x10) & 0xfffffffe;
                    /* WARNING: Could not recover jumptable at 0x00420fc3. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  DuiLib::CDuiString::~CDuiString(*(CDuiString **)(unaff_EBP + -0x14));
  return;
}


