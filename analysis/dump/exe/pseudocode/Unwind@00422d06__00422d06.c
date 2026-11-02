// Program: SM809 mouse Software.exe
// Function: Unwind@00422d06
// Entry: 00422d06
// Body: 00422d06 - 00422d0e
// Signature: undefined Unwind@00422d06(void)


void Unwind_00422d06(void)

{
  int unaff_EBP;
  
                    /* WARNING: Could not recover jumptable at 0x00422d09. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  DuiLib::CNotifyPump::~CNotifyPump(*(CNotifyPump **)(unaff_EBP + -0x14));
  return;
}


