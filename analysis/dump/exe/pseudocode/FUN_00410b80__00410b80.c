// Program: SM809 mouse Software.exe
// Function: FUN_00410b80
// Entry: 00410b80
// Body: 00410b80 - 00410c9e
// Signature: undefined FUN_00410b80(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_00410b80(int param_1)

{
  CDuiString *pCVar1;
  wchar_t *_Str;
  int iVar2;
  DWORD DVar3;
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_004228bd;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  *(undefined4 *)(param_1 + 0x2a8) = 1;
  *(undefined4 *)(param_1 + 0x2ac) = 1;
  (**(code **)(**(int **)(param_1 + 0x35c) + 0x2c))(L"stop_recording_text",local_14);
  DuiLib::CDuiString::CDuiString(local_98);
  local_8 = 0;
  pCVar1 = (CDuiString *)(**(code **)(**(int **)(param_1 + 0x358) + 0x28))(local_11c);
  local_8._0_1_ = 1;
  DuiLib::CDuiString::operator=(local_98,pCVar1);
  local_8 = (uint)local_8._1_3_ << 8;
  DuiLib::CDuiString::~CDuiString(local_11c);
  _Str = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
  iVar2 = _wtoi(_Str);
  *(short *)(param_1 + 0x2b8) = (short)iVar2;
  (**(code **)(param_1 + 0x324))(*(undefined4 *)(param_1 + 0x14));
  (**(code **)(param_1 + 0x318))(*(undefined4 *)(param_1 + 0x14));
  (**(code **)(param_1 + 0x32c))(1);
  if (*(int *)(param_1 + 0x2ec) == 0) {
    DVar3 = GetTickCount();
    *(DWORD *)(param_1 + 0x2c8) = DVar3;
  }
  else {
    QueryPerformanceCounter((LARGE_INTEGER *)(param_1 + 0x2d8));
  }
  DuiLib::CDuiString::~CDuiString(local_98);
  ExceptionList = local_10;
  return;
}


