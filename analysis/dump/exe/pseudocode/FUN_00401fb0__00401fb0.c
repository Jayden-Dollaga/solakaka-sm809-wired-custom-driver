// Program: SM809 mouse Software.exe
// Function: FUN_00401fb0
// Entry: 00401fb0
// Body: 00401fb0 - 004020ca
// Signature: CDuiString * FUN_00401fb0(CDuiString * param_1)


/* WARNING: Function: __alloca_probe replaced with injection: alloca_probe */
/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

CDuiString * __fastcall FUN_00401fb0(CDuiString *param_1)

{
  CDuiString local_1bf0 [132];
  wchar_t local_1b6c [500];
  wchar_t local_1784 [500];
  wchar_t local_139c [500];
  wchar_t local_fb4 [500];
  wchar_t local_bcc [500];
  wchar_t local_7e4 [500];
  WCHAR local_3fc [500];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00420f81;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_3fc + 0x1fc);
  ExceptionList = &local_10;
  DuiLib::CDuiString::CDuiString(local_1bf0);
  local_8 = 0;
  GetModuleFileNameW((HMODULE)0x0,local_3fc,500);
  _wsplitpath_s(local_3fc,local_bcc,500,local_7e4,500,local_1b6c,500,local_1784,500);
  _wmakepath_s(local_fb4,500,local_bcc,local_7e4,(wchar_t *)0x0,(wchar_t *)0x0);
  wcscpy_s(local_139c,500,local_fb4);
  DuiLib::CDuiString::CDuiString(param_1,local_139c,-1);
  DuiLib::CDuiString::~CDuiString(local_1bf0);
  ExceptionList = local_10;
  return param_1;
}


