// Program: SM809 mouse Software.exe
// Function: FUN_00405a30
// Entry: 00405a30
// Body: 00405a30 - 00405b68
// Signature: undefined4 * FUN_00405a30(void * this, undefined4 param_1, undefined4 param_2, undefined1 param_3)


undefined4 * __thiscall
FUN_00405a30(void *this,undefined4 param_1,undefined4 param_2,undefined1 param_3)

{
  size_t _Size;
  uint uVar1;
  void *pvVar2;
  uint uVar3;
  void *_Dst;
  uint uVar4;
  void *pvVar5;
  
  _Size = *(size_t *)((int)this + 0x10);
  if (_Size == 0x7fffffff) {
    FUN_00405cd0();
LAB_00405b64:
                    /* WARNING: Subroutine does not return */
    FUN_00405dc0();
  }
  uVar1 = *(uint *)((int)this + 0x14);
  uVar4 = _Size + 1 | 0xf;
  if (uVar4 < 0x80000000) {
    if (0x7fffffff - (uVar1 >> 1) < uVar1) {
      uVar4 = 0x7fffffff;
    }
    else {
      uVar3 = (uVar1 >> 1) + uVar1;
      if (uVar4 < uVar3) {
        uVar4 = uVar3;
      }
    }
  }
  else {
    uVar4 = 0x7fffffff;
  }
  uVar3 = -(uint)(0xfffffffe < uVar4) | uVar4 + 1;
  if (uVar3 < 0x1000) {
    if (uVar3 == 0) {
      _Dst = (void *)0x0;
    }
    else {
      _Dst = operator_new(uVar3);
    }
  }
  else {
    if (uVar3 + 0x23 <= uVar3) goto LAB_00405b64;
    pvVar2 = operator_new(uVar3 + 0x23);
    if (pvVar2 == (void *)0x0) goto LAB_00405b34;
    _Dst = (void *)((int)pvVar2 + 0x23U & 0xffffffe0);
    *(void **)((int)_Dst - 4) = pvVar2;
  }
  *(size_t *)((int)this + 0x10) = _Size + 1;
  *(uint *)((int)this + 0x14) = uVar4;
  if (uVar1 < 0x10) {
    memcpy(_Dst,this,_Size);
    *(undefined1 *)((int)_Dst + _Size) = param_3;
    *(undefined1 *)((int)_Dst + _Size + 1) = 0;
    *(void **)this = _Dst;
    return this;
  }
  pvVar2 = *(void **)this;
  memcpy(_Dst,pvVar2,_Size);
  *(undefined1 *)((int)_Dst + _Size) = param_3;
  *(undefined1 *)((int)_Dst + _Size + 1) = 0;
  pvVar5 = pvVar2;
  if ((uVar1 + 1 < 0x1000) ||
     (pvVar5 = *(void **)((int)pvVar2 + -4), (uint)((int)pvVar2 + (-4 - (int)pvVar5)) < 0x20)) {
    FUN_0041feb7(pvVar5);
    *(void **)this = _Dst;
    return this;
  }
LAB_00405b34:
                    /* WARNING: Subroutine does not return */
  _invalid_parameter_noinfo_noreturn();
}


