// Program: SM809 mouse Software.exe
// Function: FUN_00423d80
// Entry: 00423d80
// Body: 00423d80 - 00423ddc
// Signature: undefined FUN_00423d80(void)


void FUN_00423d80(void)

{
  void *pvVar1;
  
  if (DAT_0046c398 != (void *)0x0) {
    pvVar1 = DAT_0046c398;
    if ((0xfff < (DAT_0046c3a0 - (int)DAT_0046c398 & 0xfffffffcU)) &&
       (pvVar1 = *(void **)((int)DAT_0046c398 + -4),
       0x1f < (uint)((int)DAT_0046c398 + (-4 - (int)pvVar1)))) {
                    /* WARNING: Could not recover jumptable at 0x00423dd7. Too many branches */
                    /* WARNING: Subroutine does not return */
                    /* WARNING: Treating indirect jump as call */
      _invalid_parameter_noinfo_noreturn();
      return;
    }
    FUN_0041feb7(pvVar1);
    DAT_0046c398 = (void *)0x0;
    DAT_0046c39c = 0;
    DAT_0046c3a0 = 0;
  }
  return;
}


