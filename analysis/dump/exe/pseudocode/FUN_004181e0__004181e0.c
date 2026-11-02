// Program: SM809 mouse Software.exe
// Function: FUN_004181e0
// Entry: 004181e0
// Body: 004181e0 - 004183e1
// Signature: undefined FUN_004181e0(void * this, int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_004181e0(void *this,int param_1)

{
  void *_Src;
  void *_Dst;
  uint uVar1;
  CControlUI *pCVar2;
  int iVar3;
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
  puStack_c = &LAB_004235b0;
  local_10 = ExceptionList;
  uVar1 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  if (1 < (uint)(DAT_0046c390 - DAT_0046c38c >> 2)) {
    local_14 = uVar1;
    pCVar2 = DuiLib::CPaintManagerUI::FindControl
                       ((CPaintManagerUI *)((int)this + 0x30),L"disable_window_ver");
    (**(code **)(*(int *)pCVar2 + 0xf8))(1,uVar1);
    memset(local_898,0,0x884);
    FUN_0041c1c0((WindowImplBase *)local_898);
    local_8 = 0;
    DuiLib::CDuiString::operator=(local_11c,L"warning_title_text");
    DuiLib::CDuiString::operator=(local_98,L"delete_profile_text");
    DuiLib::CWindowWnd::Create
              ((CWindowWnd *)local_898,*(HWND__ **)((int)this + 4),L"MsgWnd",0x90000000,0x80,0,0,800
               ,800,(HMENU__ *)0x0);
    DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_898);
    uVar1 = DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_898);
    if (uVar1 == 1) {
      if (DAT_0046c38c != DAT_0046c390) {
        _Dst = (void *)(DAT_0046c38c + param_1 * 4);
        _Src = (void *)((int)_Dst + 4);
        memmove(_Dst,_Src,DAT_0046c390 - (int)_Src);
        DAT_0046c390 = DAT_0046c390 + -4;
        FUN_004035a0();
      }
      *(undefined4 *)((int)this + 0x1580) = 1;
      (**(code **)(*(int *)(*(int *)((int)this + 0x16fc) + 0x558) + 0x1c))(param_1);
      iVar3 = param_1 + -1;
      if (param_1 < DAT_0046c390 - DAT_0046c38c >> 2) {
        iVar3 = param_1;
      }
      (**(code **)(*(int *)(*(int *)((int)this + 0x16fc) + 0x6a0) + 0xc))(iVar3,0);
    }
    (**(code **)(*(int *)pCVar2 + 0xf8))(0);
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


