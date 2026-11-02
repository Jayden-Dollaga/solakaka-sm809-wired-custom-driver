// Program: SM809 mouse Software.exe
// Function: FUN_00404790
// Entry: 00404790
// Body: 00404790 - 00404879
// Signature: __int64 FUN_00404790(void * this, char * param_1, uint param_2, int param_3)


__int64 __thiscall FUN_00404790(void *this,char *param_1,uint param_2,int param_3)

{
  size_t sVar1;
  uint _Count;
  undefined4 unaff_EDI;
  int iVar2;
  bool bVar3;
  __int64 _Var4;
  uint local_1c;
  int local_18;
  
  if (*(int *)((int)this + 0x38) != 0) {
    _Var4 = std::basic_streambuf<char,std::char_traits<char>_>::xsputn
                      (this,param_1,CONCAT44(unaff_EDI,param_3));
    return _Var4;
  }
  if ((void *)**(undefined4 **)((int)this + 0x20) == (void *)0x0) {
    local_1c = 0;
  }
  else {
    local_1c = **(uint **)((int)this + 0x30);
  }
  local_18 = (int)local_1c >> 0x1f;
  _Count = param_2;
  iVar2 = param_3;
  if ((param_3 < 0) || ((param_3 < 1 && (param_2 == 0)))) goto LAB_00404865;
  if ((-1 < local_18) && ((0 < local_18 || (local_1c != 0)))) {
    if ((param_3 <= local_18) && ((param_3 < local_18 || (param_2 < local_1c)))) {
      local_1c = param_2;
      local_18 = param_3;
    }
    memcpy((void *)**(undefined4 **)((int)this + 0x20),param_1,local_1c);
    _Count = param_2 - local_1c;
    iVar2 = (param_3 - local_18) - (uint)(param_2 < local_1c);
    param_1 = param_1 + local_1c;
    **(int **)((int)this + 0x30) = **(int **)((int)this + 0x30) - local_1c;
    **(int **)((int)this + 0x20) = **(int **)((int)this + 0x20) + local_1c;
    if (iVar2 < 0) goto LAB_00404865;
    if ((iVar2 < 1) && (_Count == 0)) goto LAB_00404865;
  }
  if (*(FILE **)((int)this + 0x4c) != (FILE *)0x0) {
    sVar1 = fwrite(param_1,1,_Count,*(FILE **)((int)this + 0x4c));
    bVar3 = _Count < sVar1;
    _Count = _Count - sVar1;
    iVar2 = iVar2 - (uint)bVar3;
  }
LAB_00404865:
  return CONCAT44((param_3 - iVar2) - (uint)(param_2 < _Count),param_2 - _Count);
}


