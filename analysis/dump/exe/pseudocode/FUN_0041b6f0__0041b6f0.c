// Program: SM809 mouse Software.exe
// Function: FUN_0041b6f0
// Entry: 0041b6f0
// Body: 0041b6f0 - 0041b846
// Signature: undefined FUN_0041b6f0(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_0041b6f0(int param_1)

{
  undefined **local_898 [4];
  undefined **local_888;
  undefined **local_878;
  undefined **local_874;
  undefined **local_870;
  undefined **local_86c;
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00423690;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  if (DAT_00432ac8 != 1) {
    DAT_00432ac8 = 1;
    memset(local_898,0,0x884);
    FUN_0041c1c0((WindowImplBase *)local_898);
    local_8 = 0;
    DuiLib::CDuiString::operator=(local_11c,L"warning_title_text");
    DuiLib::CDuiString::operator=(local_98,L"no_connect_device_text");
    DuiLib::CWindowWnd::Create
              ((CWindowWnd *)local_898,*(HWND__ **)(param_1 + 4),L"MsgWnd",0x90000000,0x80,0,0,800,
               800,(HMENU__ *)0x0);
    DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_898);
    DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_898);
    DAT_00432ac8 = 0;
    local_898[0] = CMsgWnd::vftable;
    local_888 = CMsgWnd::vftable;
    local_878 = CMsgWnd::vftable;
    local_874 = CMsgWnd::vftable;
    local_870 = CMsgWnd::vftable;
    local_86c = CMsgWnd::vftable;
    DuiLib::CDuiString::~CDuiString(local_98);
    DuiLib::CDuiString::~CDuiString(local_11c);
    DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_898);
  }
  ExceptionList = local_10;
  return;
}


