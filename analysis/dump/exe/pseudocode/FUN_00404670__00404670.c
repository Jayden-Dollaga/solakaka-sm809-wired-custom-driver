// Program: SM809 mouse Software.exe
// Function: FUN_00404670
// Entry: 00404670
// Body: 00404670 - 0040478c
// Signature: undefined4 * FUN_00404670(void * this, undefined4 * param_1, int param_2, int param_3, int param_4)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

undefined4 * __thiscall
FUN_00404670(void *this,undefined4 *param_1,int param_2,int param_3,int param_4)

{
  int iVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  int iVar4;
  int unaff_EDI;
  bool bVar5;
  int local_1c;
  undefined4 local_18;
  undefined4 local_14;
  uint local_c;
  
  local_c = DAT_00432008 ^ (uint)&local_1c;
  if (((**(int **)((int)this + 0x1c) == (int)this + 0x3c) && (param_4 == 1)) &&
     (*(int *)((int)this + 0x38) == 0)) {
    bVar5 = param_2 != 0;
    param_2 = param_2 + -1;
    param_3 = param_3 + -1 + (uint)bVar5;
  }
  if (*(int *)((int)this + 0x4c) != 0) {
    local_1c = param_3;
    bVar5 = FUN_00405100(this);
    if (((bVar5) &&
        (((param_2 == 0 && local_1c == 0 && (param_4 == 1)) ||
         (iVar4 = _fseeki64(*(FILE **)((int)this + 0x4c),CONCAT44(param_4,local_1c),unaff_EDI),
         iVar4 == 0)))) &&
       (iVar4 = fgetpos(*(FILE **)((int)this + 0x4c),(fpos_t *)&local_18), iVar4 == 0)) {
      if (**(int **)((int)this + 0xc) == (int)this + 0x3c) {
        iVar4 = *(int *)((int)this + 0x54);
        iVar1 = *(int *)((int)this + 0x50);
        **(int **)((int)this + 0xc) = iVar1;
        **(int **)((int)this + 0x1c) = iVar1;
        **(int **)((int)this + 0x2c) = iVar4 - iVar1;
      }
      uVar2 = *(undefined4 *)((int)this + 0x40);
      uVar3 = *(undefined4 *)((int)this + 0x44);
      *param_1 = local_18;
      param_1[1] = local_14;
      param_1[2] = 0;
      param_1[3] = 0;
      param_1[4] = uVar2;
      param_1[5] = uVar3;
      return param_1;
    }
  }
  *param_1 = 0xffffffff;
  param_1[1] = 0xffffffff;
  param_1[2] = 0;
  param_1[3] = 0;
  *(undefined8 *)(param_1 + 4) = 0;
  return param_1;
}


