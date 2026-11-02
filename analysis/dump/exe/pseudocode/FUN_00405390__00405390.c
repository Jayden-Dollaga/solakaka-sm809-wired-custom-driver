// Program: SM809 mouse Software.exe
// Function: FUN_00405390
// Entry: 00405390
// Body: 00405390 - 00405506
// Signature: undefined4 * FUN_00405390(void * param_1, undefined4 * param_2)


undefined4 * FUN_00405390(void *param_1,undefined4 *param_2)

{
  uint uVar1;
  undefined4 *puVar2;
  int iVar3;
  void *pvVar4;
  uint uVar5;
  int iVar6;
  void *_Dst;
  uint uVar7;
  
  iVar6 = (int)param_1 - (int)DAT_0046c38c;
  iVar3 = (int)DAT_0046c390 - (int)DAT_0046c38c >> 2;
  if (iVar3 == 0x3fffffff) {
                    /* WARNING: Subroutine does not return */
    FUN_00405900();
  }
  uVar1 = iVar3 + 1;
  uVar5 = (int)DAT_0046c394 - (int)DAT_0046c38c >> 2;
  if (0x3fffffff - (uVar5 >> 1) < uVar5) {
LAB_004054fd:
                    /* WARNING: Subroutine does not return */
    FUN_00405dc0();
  }
  uVar5 = (uVar5 >> 1) + uVar5;
  uVar7 = uVar1;
  if (uVar1 <= uVar5) {
    uVar7 = uVar5;
  }
  if (0x3fffffff < uVar7) goto LAB_004054fd;
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
    if (uVar7 + 0x23 <= uVar7) goto LAB_004054fd;
    pvVar4 = operator_new(uVar7 + 0x23);
    if (pvVar4 == (void *)0x0) goto LAB_004054f7;
    _Dst = (void *)((int)pvVar4 + 0x23U & 0xffffffe0);
    *(void **)((int)_Dst - 4) = pvVar4;
  }
  puVar2 = (undefined4 *)((int)_Dst + (iVar6 >> 2) * 4);
  *puVar2 = *param_2;
  if (param_1 == DAT_0046c390) {
    memmove(_Dst,DAT_0046c38c,(int)DAT_0046c390 - (int)DAT_0046c38c);
  }
  else {
    memmove(_Dst,DAT_0046c38c,(int)param_1 - (int)DAT_0046c38c);
    memmove(puVar2 + 1,param_1,(int)DAT_0046c390 - (int)param_1);
  }
  if (DAT_0046c38c != (void *)0x0) {
    pvVar4 = DAT_0046c38c;
    if ((0xfff < ((int)DAT_0046c394 - (int)DAT_0046c38c & 0xfffffffcU)) &&
       (pvVar4 = *(void **)((int)DAT_0046c38c + -4),
       0x1f < (uint)((int)DAT_0046c38c + (-4 - (int)pvVar4)))) {
LAB_004054f7:
                    /* WARNING: Subroutine does not return */
      _invalid_parameter_noinfo_noreturn();
    }
    FUN_0041feb7(pvVar4);
  }
  DAT_0046c38c = _Dst;
  DAT_0046c390 = (void *)((int)_Dst + uVar1 * 4);
  DAT_0046c394 = (void *)(uVar7 + (int)_Dst);
  return puVar2;
}


