// Program: SM809 mouse Software.exe
// Function: Unwind@004214e0
// Entry: 004214e0
// Body: 004214e0 - 004214fc
// Signature: undefined Unwind@004214e0(void)


void Unwind_004214e0(void)

{
  int unaff_EBP;
  
  if ((*(uint *)(unaff_EBP + -0x10) & 1) == 0) {
    return;
  }
  *(uint *)(unaff_EBP + -0x10) = *(uint *)(unaff_EBP + -0x10) & 0xfffffffe;
                    /* WARNING: Could not recover jumptable at 0x004214f6. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  std::basic_ios<char,std::char_traits<char>_>::~basic_ios<char,std::char_traits<char>_>
            ((basic_ios<char,std::char_traits<char>_> *)(*(int *)(unaff_EBP + -0x14) + 0x68));
  return;
}


