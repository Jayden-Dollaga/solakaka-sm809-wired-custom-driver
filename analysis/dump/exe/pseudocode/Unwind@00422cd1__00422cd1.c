// Program: SM809 mouse Software.exe
// Function: Unwind@00422cd1
// Entry: 00422cd1
// Body: 00422cd1 - 00422cd9
// Signature: undefined Unwind@00422cd1(void)


void Unwind_00422cd1(void)

{
  int unaff_EBP;
  
                    /* WARNING: Could not recover jumptable at 0x00422cd4. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  DuiLib::CNotifyPump::~CNotifyPump(*(CNotifyPump **)(unaff_EBP + -0x14));
  return;
}


