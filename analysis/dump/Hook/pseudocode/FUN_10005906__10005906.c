// Program: Hook.dll
// Function: FUN_10005906
// Entry: 10005906
// Body: 10005906 - 100059d0
// Signature: uint FUN_10005906(void * this, uint param_1)


uint __thiscall FUN_10005906(void *this,uint param_1)

{
  uint uVar1;
  uint uVar2;
  int iVar3;
  void *local_8;
  
  uVar1 = param_1;
  if (DAT_10007f1c == 0) {
    if ((int)param_1 < 0x41) {
      return param_1;
    }
    if ((int)param_1 < 0x5b) {
      return param_1 + 0x20;
    }
    return param_1;
  }
  iVar3 = 1;
  local_8 = this;
  if ((int)param_1 < 0x100) {
    if (DAT_10007ac4 < 2) {
      uVar2 = (byte)PTR_DAT_100073d8[param_1 * 2] & 1;
    }
    else {
      uVar2 = FUN_10005891(this,param_1,1);
    }
    if (uVar2 == 0) {
      return uVar1;
    }
  }
  if ((PTR_DAT_100073d8[((int)uVar1 >> 8 & 0xffU) * 2 + 1] & 0x80) == 0) {
    param_1 = CONCAT31((int3)(param_1 >> 8),(char)uVar1) & 0xffff00ff;
  }
  else {
    uVar2 = param_1 >> 0x10;
    param_1._0_2_ = CONCAT11((char)uVar1,(char)(uVar1 >> 8));
    param_1 = CONCAT22((short)uVar2,(undefined2)param_1) & 0xff00ffff;
    iVar3 = 2;
  }
  iVar3 = FUN_10004a73(DAT_10007f1c,0x100,(char *)&param_1,iVar3,(LPWSTR)&local_8,3,0,1);
  if (iVar3 == 0) {
    return uVar1;
  }
  if (iVar3 == 1) {
    return (uint)local_8 & 0xff;
  }
  return (uint)local_8 & 0xffff;
}


