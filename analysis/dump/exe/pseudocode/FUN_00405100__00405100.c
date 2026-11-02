// Program: SM809 mouse Software.exe
// Function: FUN_00405100
// Entry: 00405100
// Body: 00405100 - 004051cc
// Signature: bool FUN_00405100(int * param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

bool __fastcall FUN_00405100(int *param_1)

{
  int iVar1;
  size_t sVar2;
  size_t _Count;
  char *local_2c;
  char local_28 [32];
  undefined4 local_8;
  
  local_8 = DAT_00432008 ^ (uint)(local_28 + 0x24);
  if ((param_1[0xe] == 0) || (*(char *)((int)param_1 + 0x3d) == '\0')) {
    return true;
  }
  iVar1 = (**(code **)(*param_1 + 0xc))(0xffffffff);
  if (iVar1 == -1) {
    return false;
  }
  iVar1 = std::codecvt<char,char,_Mbstatet>::unshift
                    ((codecvt<char,char,_Mbstatet> *)param_1[0xe],(_Mbstatet *)(param_1 + 0x10),
                     local_28,(char *)&local_8,&local_2c);
  if (iVar1 == 0) {
    *(undefined1 *)((int)param_1 + 0x3d) = 0;
  }
  else if (iVar1 != 1) {
    if (iVar1 == 3) {
      *(undefined1 *)((int)param_1 + 0x3d) = 0;
      return true;
    }
    return false;
  }
  _Count = (int)local_2c - (int)local_28;
  if ((_Count == 0) || (sVar2 = fwrite(local_28,1,_Count,(FILE *)param_1[0x13]), _Count == sVar2)) {
    return *(char *)((int)param_1 + 0x3d) == '\0';
  }
  return false;
}


