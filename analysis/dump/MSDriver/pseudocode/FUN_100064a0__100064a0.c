// Program: MSDriver.dll
// Function: FUN_100064a0
// Entry: 100064a0
// Body: 100064a0 - 1000656f
// Signature: uint FUN_100064a0(void * this, byte * param_1, byte * param_2)


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

uint __thiscall FUN_100064a0(void *this,byte *param_1,byte *param_2)

{
  bool bVar1;
  int iVar2;
  byte bVar3;
  byte bVar4;
  byte bVar5;
  char cVar6;
  uint uVar7;
  void *extraout_ECX;
  void *this_00;
  void *extraout_ECX_00;
  uint uVar8;
  uint uVar9;
  
  iVar2 = _DAT_1000a254;
  if (DAT_1000a0f0 == 0) {
    bVar5 = 0xff;
    do {
      do {
        cVar6 = '\0';
        if (bVar5 == 0) goto LAB_100064ee;
        bVar5 = *param_2;
        param_2 = param_2 + 1;
        bVar4 = *param_1;
        param_1 = param_1 + 1;
      } while (bVar4 == bVar5);
      bVar3 = bVar5 + 0xbf + (-((byte)(bVar5 + 0xbf) < 0x1a) & 0x20U) + 0x41;
      bVar4 = bVar4 + 0xbf;
      bVar5 = bVar4 + (-(bVar4 < 0x1a) & 0x20U) + 0x41;
    } while (bVar5 == bVar3);
    cVar6 = (bVar5 < bVar3) * -2 + '\x01';
LAB_100064ee:
    uVar7 = (uint)cVar6;
  }
  else {
    LOCK();
    _DAT_1000a254 = _DAT_1000a254 + 1;
    UNLOCK();
    bVar1 = 0 < DAT_1000a250;
    if (bVar1) {
      LOCK();
      UNLOCK();
      _DAT_1000a254 = iVar2;
      FUN_1000277c(0x13);
      this = extraout_ECX;
    }
    uVar9 = (uint)bVar1;
    uVar7 = 0xff;
    uVar8 = 0;
    do {
      do {
        if ((char)uVar7 == '\0') goto LAB_1000654f;
        bVar5 = *param_2;
        uVar7 = CONCAT31((int3)(uVar7 >> 8),bVar5);
        param_2 = param_2 + 1;
        bVar4 = *param_1;
        uVar8 = CONCAT31((int3)(uVar8 >> 8),bVar4);
        param_1 = param_1 + 1;
      } while (bVar5 == bVar4);
      uVar8 = FUN_100066e6(this,uVar8);
      uVar7 = FUN_100066e6(this_00,uVar7);
      this = extraout_ECX_00;
    } while ((byte)uVar8 == (byte)uVar7);
    uVar8 = (uint)((byte)uVar8 < (byte)uVar7);
    uVar7 = (1 - uVar8) - (uint)(uVar8 != 0);
LAB_1000654f:
    if (uVar9 == 0) {
      LOCK();
      _DAT_1000a254 = _DAT_1000a254 + -1;
      UNLOCK();
    }
    else {
      FUN_100027dd(0x13);
    }
  }
  return uVar7;
}


