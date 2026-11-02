// Program: SM809 mouse Software.exe
// Function: FUN_00423cc0
// Entry: 00423cc0
// Body: 00423cc0 - 00423d1c
// Signature: undefined FUN_00423cc0(void)


void FUN_00423cc0(void)

{
  void *pvVar1;
  
  if (DAT_0046c380 != (void *)0x0) {
    pvVar1 = DAT_0046c380;
    if ((0xfff < (DAT_0046c388 - (int)DAT_0046c380 & 0xfffffffcU)) &&
       (pvVar1 = *(void **)((int)DAT_0046c380 + -4),
       0x1f < (uint)((int)DAT_0046c380 + (-4 - (int)pvVar1)))) {
                    /* WARNING: Could not recover jumptable at 0x00423d17. Too many branches */
                    /* WARNING: Subroutine does not return */
                    /* WARNING: Treating indirect jump as call */
      _invalid_parameter_noinfo_noreturn();
      return;
    }
    FUN_0041feb7(pvVar1);
    DAT_0046c380 = (void *)0x0;
    DAT_0046c384 = 0;
    DAT_0046c388 = 0;
  }
  return;
}


