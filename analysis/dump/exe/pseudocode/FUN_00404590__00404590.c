// Program: SM809 mouse Software.exe
// Function: FUN_00404590
// Entry: 00404590
// Body: 00404590 - 0040466f
// Signature: int * FUN_00404590(void * this, int * param_1, uint param_2, int param_3, uint param_4, int param_5, int param_6, int param_7)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

int * __thiscall
FUN_00404590(void *this,int *param_1,uint param_2,int param_3,uint param_4,int param_5,int param_6,
            int param_7)

{
  int iVar1;
  bool bVar2;
  int iVar3;
  undefined1 auStack_1c [4];
  int local_18;
  int local_14;
  uint local_c;
  
  local_c = DAT_00432008 ^ (uint)auStack_1c;
  local_18 = param_2 + param_4;
  local_14 = param_3 + param_5 + (uint)CARRY4(param_2,param_4);
  if (((*(int *)((int)this + 0x4c) != 0) && (bVar2 = FUN_00405100(this), bVar2)) &&
     (iVar3 = fsetpos(*(FILE **)((int)this + 0x4c),(fpos_t *)&local_18), iVar3 == 0)) {
    *(int *)((int)this + 0x40) = param_6;
    *(int *)((int)this + 0x44) = param_7;
    if (**(int **)((int)this + 0xc) == (int)this + 0x3c) {
      iVar3 = *(int *)((int)this + 0x54);
      iVar1 = *(int *)((int)this + 0x50);
      **(int **)((int)this + 0xc) = iVar1;
      **(int **)((int)this + 0x1c) = iVar1;
      **(int **)((int)this + 0x2c) = iVar3 - iVar1;
    }
    iVar3 = *(int *)((int)this + 0x40);
    iVar1 = *(int *)((int)this + 0x44);
    *param_1 = local_18;
    param_1[1] = local_14;
    param_1[2] = 0;
    param_1[3] = 0;
    param_1[4] = iVar3;
    param_1[5] = iVar1;
    return param_1;
  }
  *param_1 = -1;
  param_1[1] = -1;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  param_1[5] = 0;
  return param_1;
}


