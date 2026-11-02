// Program: SM809 mouse Software.exe
// Function: FUN_00423d20
// Entry: 00423d20
// Body: 00423d20 - 00423d7c
// Signature: undefined FUN_00423d20(void)


void FUN_00423d20(void)

{
  void *pvVar1;
  
  if (DAT_0046c38c != (void *)0x0) {
    pvVar1 = DAT_0046c38c;
    if ((0xfff < (DAT_0046c394 - (int)DAT_0046c38c & 0xfffffffcU)) &&
       (pvVar1 = *(void **)((int)DAT_0046c38c + -4),
       0x1f < (uint)((int)DAT_0046c38c + (-4 - (int)pvVar1)))) {
                    /* WARNING: Could not recover jumptable at 0x00423d77. Too many branches */
                    /* WARNING: Subroutine does not return */
                    /* WARNING: Treating indirect jump as call */
      _invalid_parameter_noinfo_noreturn();
      return;
    }
    FUN_0041feb7(pvVar1);
    DAT_0046c38c = (void *)0x0;
    DAT_0046c390 = 0;
    DAT_0046c394 = 0;
  }
  return;
}


