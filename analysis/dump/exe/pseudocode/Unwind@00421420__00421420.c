// Program: SM809 mouse Software.exe
// Function: Unwind@00421420
// Entry: 00421420
// Body: 00421420 - 0042143c
// Signature: undefined Unwind@00421420(void)


void Unwind_00421420(void)

{
  int unaff_EBP;
  
  if ((*(uint *)(unaff_EBP + -0x10) & 1) == 0) {
    return;
  }
  *(uint *)(unaff_EBP + -0x10) = *(uint *)(unaff_EBP + -0x10) & 0xfffffffe;
                    /* WARNING: Could not recover jumptable at 0x00421436. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  std::basic_ios<char,std::char_traits<char>_>::~basic_ios<char,std::char_traits<char>_>
            ((basic_ios<char,std::char_traits<char>_> *)(*(int *)(unaff_EBP + -0x14) + 0x70));
  return;
}


