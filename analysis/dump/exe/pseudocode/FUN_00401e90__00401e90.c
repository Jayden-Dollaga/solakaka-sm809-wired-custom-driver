// Program: SM809 mouse Software.exe
// Function: FUN_00401e90
// Entry: 00401e90
// Body: 00401e90 - 00401fa6
// Signature: CDuiString * FUN_00401e90(CDuiString * param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

CDuiString * __fastcall FUN_00401e90(CDuiString *param_1)

{
  CDuiString local_ed0 [132];
  wchar_t local_e4c [260];
  wchar_t local_c44 [260];
  wchar_t local_a3c [260];
  wchar_t local_834 [260];
  wchar_t local_62c [260];
  wchar_t local_424 [260];
  WCHAR local_21c [260];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00420f41;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_21c + 0x10c);
  ExceptionList = &local_10;
  DuiLib::CDuiString::CDuiString(local_ed0);
  local_8 = 0;
  GetModuleFileNameW((HMODULE)0x0,local_21c,0x104);
  _wsplitpath_s(local_21c,local_62c,0x104,local_424,0x104,local_e4c,0x104,local_c44,0x104);
  _wmakepath_s(local_834,0x104,local_62c,local_424,(wchar_t *)0x0,(wchar_t *)0x0);
  wcscpy_s(local_a3c,0x104,local_834);
  DuiLib::CDuiString::CDuiString(param_1,local_a3c,-1);
  DuiLib::CDuiString::~CDuiString(local_ed0);
  ExceptionList = local_10;
  return param_1;
}


