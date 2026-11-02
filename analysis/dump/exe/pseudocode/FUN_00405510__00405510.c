// Program: SM809 mouse Software.exe
// Function: FUN_00405510
// Entry: 00405510
// Body: 00405510 - 00405686
// Signature: undefined4 * FUN_00405510(void * param_1, undefined4 * param_2)


undefined4 * FUN_00405510(void *param_1,undefined4 *param_2)

{
  uint uVar1;
  undefined4 *puVar2;
  int iVar3;
  void *pvVar4;
  uint uVar5;
  int iVar6;
  void *_Dst;
  uint uVar7;
  
  iVar6 = (int)param_1 - (int)DAT_0046c398;
  iVar3 = (int)DAT_0046c39c - (int)DAT_0046c398 >> 2;
  if (iVar3 == 0x3fffffff) {
                    /* WARNING: Subroutine does not return */
    FUN_00405900();
  }
  uVar1 = iVar3 + 1;
  uVar5 = (int)DAT_0046c3a0 - (int)DAT_0046c398 >> 2;
  if (0x3fffffff - (uVar5 >> 1) < uVar5) {
LAB_0040567d:
                    /* WARNING: Subroutine does not return */
    FUN_00405dc0();
  }
  uVar5 = (uVar5 >> 1) + uVar5;
  uVar7 = uVar1;
  if (uVar1 <= uVar5) {
    uVar7 = uVar5;
  }
  if (0x3fffffff < uVar7) goto LAB_0040567d;
  uVar7 = uVar7 * 4;
  if (uVar7 < 0x1000) {
    if (uVar7 == 0) {
      _Dst = (void *)0x0;
    }
    else {
      _Dst = operator_new(uVar7);
    }
  }
  else {
    if (uVar7 + 0x23 <= uVar7) goto LAB_0040567d;
    pvVar4 = operator_new(uVar7 + 0x23);
    if (pvVar4 == (void *)0x0) goto LAB_00405677;
    _Dst = (void *)((int)pvVar4 + 0x23U & 0xffffffe0);
    *(void **)((int)_Dst - 4) = pvVar4;
  }
  puVar2 = (undefined4 *)((int)_Dst + (iVar6 >> 2) * 4);
  *puVar2 = *param_2;
  if (param_1 == DAT_0046c39c) {
    memmove(_Dst,DAT_0046c398,(int)DAT_0046c39c - (int)DAT_0046c398);
  }
  else {
    memmove(_Dst,DAT_0046c398,(int)param_1 - (int)DAT_0046c398);
    memmove(puVar2 + 1,param_1,(int)DAT_0046c39c - (int)param_1);
  }
  if (DAT_0046c398 != (void *)0x0) {
    pvVar4 = DAT_0046c398;
    if ((0xfff < ((int)DAT_0046c3a0 - (int)DAT_0046c398 & 0xfffffffcU)) &&
       (pvVar4 = *(void **)((int)DAT_0046c398 + -4),
       0x1f < (uint)((int)DAT_0046c398 + (-4 - (int)pvVar4)))) {
LAB_00405677:
                    /* WARNING: Subroutine does not return */
      _invalid_parameter_noinfo_noreturn();
    }
    FUN_0041feb7(pvVar4);
  }
  DAT_0046c398 = _Dst;
  DAT_0046c39c = (void *)((int)_Dst + uVar1 * 4);
  DAT_0046c3a0 = (void *)(uVar7 + (int)_Dst);
  return puVar2;
}


