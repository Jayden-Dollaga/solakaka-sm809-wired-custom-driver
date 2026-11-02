// Program: SM809 mouse Software.exe
// Function: FUN_00404880
// Entry: 00404880
// Body: 00404880 - 004049a5
// Signature: __int64 FUN_00404880(void * this, char * param_1, uint param_2, int param_3)


__int64 __thiscall FUN_00404880(void *this,char *param_1,uint param_2,int param_3)

{
  uint uVar1;
  int iVar2;
  int iVar3;
  size_t sVar4;
  undefined4 unaff_ESI;
  uint _Size;
  uint _Count;
  __int64 _Var5;
  char *local_8;
  
  local_8 = param_1;
  if ((param_3 < 1) && ((param_3 < 0 || (param_2 == 0)))) {
    return 0;
  }
  if (*(int *)((int)this + 0x38) != 0) {
    _Var5 = std::basic_streambuf<char,std::char_traits<char>_>::xsgetn
                      (this,param_1,CONCAT44(unaff_ESI,param_3));
    return _Var5;
  }
  _Count = param_2;
  if (((void *)**(undefined4 **)((int)this + 0x1c) != (void *)0x0) &&
     (uVar1 = **(uint **)((int)this + 0x2c), uVar1 != 0)) {
    _Size = param_2;
    if (uVar1 < param_2) {
      _Size = uVar1;
    }
    memcpy(param_1,(void *)**(undefined4 **)((int)this + 0x1c),_Size);
    _Count = param_2 - _Size;
    local_8 = param_1 + _Size;
    **(int **)((int)this + 0x2c) = **(int **)((int)this + 0x2c) - _Size;
    **(int **)((int)this + 0x1c) = **(int **)((int)this + 0x1c) + _Size;
  }
  if (*(int *)((int)this + 0x4c) != 0) {
    if (**(int **)((int)this + 0xc) == (int)this + 0x3c) {
      iVar2 = *(int *)((int)this + 0x54);
      iVar3 = *(int *)((int)this + 0x50);
      **(int **)((int)this + 0xc) = iVar3;
      **(int **)((int)this + 0x1c) = iVar3;
      **(int **)((int)this + 0x2c) = iVar2 - iVar3;
    }
    while (0xfff < _Count) {
      sVar4 = fread(local_8,1,0xfff,*(FILE **)((int)this + 0x4c));
      _Count = _Count - sVar4;
      local_8 = local_8 + sVar4;
      if (sVar4 != 0xfff) {
        return CONCAT44(param_3 - (uint)(param_2 < _Count),param_2 - _Count);
      }
    }
    if (_Count != 0) {
      sVar4 = fread(local_8,1,_Count,*(FILE **)((int)this + 0x4c));
      _Count = _Count - sVar4;
    }
  }
  return CONCAT44(param_3 - (uint)(param_2 < _Count),param_2 - _Count);
}


