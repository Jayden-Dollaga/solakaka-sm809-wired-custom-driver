// Program: SM809 mouse Software.exe
// Function: FUN_00404cf0
// Entry: 00404cf0
// Body: 00404cf0 - 00404e3b
// Signature: int FUN_00404cf0(void * this, int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

int __thiscall FUN_00404cf0(void *this,int param_1)

{
  uint uVar1;
  char *pcVar2;
  int iVar3;
  int iVar4;
  size_t sVar5;
  char cVar6;
  size_t _Count;
  char *local_34;
  char *local_30;
  char local_29;
  char local_28 [32];
  undefined4 local_8;
  
  local_8 = DAT_00432008 ^ (uint)(local_28 + 0x24);
  if (param_1 == -1) {
    return 0;
  }
  uVar1 = **(uint **)((int)this + 0x20);
  cVar6 = (char)param_1;
  if ((uVar1 != 0) && (uVar1 < **(int **)((int)this + 0x30) + uVar1)) {
    pcVar2 = std::basic_streambuf<char,std::char_traits<char>_>::_Pninc(this);
    *pcVar2 = cVar6;
    return param_1;
  }
  if (*(int *)((int)this + 0x4c) != 0) {
    if (**(int **)((int)this + 0xc) == (int)this + 0x3c) {
      iVar3 = *(int *)((int)this + 0x54);
      iVar4 = *(int *)((int)this + 0x50);
      **(int **)((int)this + 0xc) = iVar4;
      **(int **)((int)this + 0x1c) = iVar4;
      **(int **)((int)this + 0x2c) = iVar3 - iVar4;
    }
    if (*(codecvt<char,char,_Mbstatet> **)((int)this + 0x38) == (codecvt<char,char,_Mbstatet> *)0x0)
    {
LAB_00404dbd:
      iVar4 = fputc((int)cVar6,*(FILE **)((int)this + 0x4c));
      iVar3 = -1;
      if (iVar4 != -1) {
        iVar3 = param_1;
      }
      return iVar3;
    }
    local_29 = cVar6;
    iVar3 = std::codecvt<char,char,_Mbstatet>::out
                      (*(codecvt<char,char,_Mbstatet> **)((int)this + 0x38),
                       (_Mbstatet *)((int)this + 0x40),&local_29,local_28,&local_34,local_28,
                       (char *)&local_8,&local_30);
    if ((iVar3 == 0) || (iVar3 == 1)) {
      _Count = (int)local_30 - (int)local_28;
      if (((_Count == 0) ||
          (sVar5 = fwrite(local_28,1,_Count,*(FILE **)((int)this + 0x4c)), _Count == sVar5)) &&
         (*(undefined1 *)((int)this + 0x3d) = 1, local_34 != &local_29)) {
        return param_1;
      }
    }
    else if (iVar3 == 3) {
      cVar6 = local_29;
      goto LAB_00404dbd;
    }
  }
  return -1;
}


