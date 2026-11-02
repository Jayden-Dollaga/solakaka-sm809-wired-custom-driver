// Program: SM809 mouse Software.exe
// Function: FUN_0040e0c0
// Entry: 0040e0c0
// Body: 0040e0c0 - 0040e457
// Signature: undefined FUN_0040e0c0(void * this, int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_0040e0c0(void *this,int param_1)

{
  uint uVar1;
  CControlUI *pCVar2;
  int *piVar3;
  WindowImplBase *this_00;
  int iVar4;
  undefined **local_f2c [4];
  undefined **local_f1c;
  undefined **local_f0c;
  undefined **local_f08;
  undefined **local_f04;
  undefined **local_f00;
  undefined1 local_7a8;
  uint local_7a4;
  undefined **local_7a0 [4];
  undefined **local_790;
  undefined **local_780;
  undefined **local_77c;
  undefined **local_778;
  undefined **local_774;
  undefined1 local_1c;
  uint local_18;
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_0042247b;
  local_10 = ExceptionList;
  uVar1 = DAT_00432008 ^ (int)register0x00000010 - 4U;
  ExceptionList = &local_10;
  local_14 = uVar1;
  if (*(int *)(param_1 + 0x108) == *(int *)((int)this + 0x70)) {
    pCVar2 = DuiLib::CPaintManagerUI::FindControl
                       (*(CPaintManagerUI **)((int)this + 0x10),L"disable_window_ver");
    (**(code **)(*(int *)pCVar2 + 0xf8))(1);
    memset(local_7a0,0,0x78c);
    DuiLib::WindowImplBase::WindowImplBase((WindowImplBase *)local_7a0);
    local_7a0[0] = CSelectColorWnd::vftable;
    local_790 = CSelectColorWnd::vftable;
    local_780 = CSelectColorWnd::vftable;
    local_77c = CSelectColorWnd::vftable;
    local_778 = CSelectColorWnd::vftable;
    local_774 = CSelectColorWnd::vftable;
    local_1c = 0;
    local_8 = 0;
    local_18 = (*(uint *)(DAT_00432aa0 + 0x104) | 0xffffff00) << 0x10 |
               (uint)*(byte *)(DAT_00432aa0 + 0x106) | *(uint *)(DAT_00432aa0 + 0x104) & 0xff00;
    DuiLib::CWindowWnd::Create
              ((CWindowWnd *)local_7a0,*(HWND__ **)((int)this + 0x14),L"SelectColorWnd",0x90000000,
               0x80,0,0,800,800,(HMENU__ *)0x0);
    DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_7a0);
    uVar1 = DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_7a0);
    if (uVar1 == 1) {
      DuiLib::CControlUI::SetBkColor(*(CControlUI **)((int)this + 0x70),local_18);
      *(uint *)(DAT_00432aa0 + 0x104) =
           ((local_18 & 0xff) << 8 | local_18 >> 8 & 0xff) << 8 | local_18 >> 0x10 & 0xff;
    }
    (**(code **)(*(int *)pCVar2 + 0xf8))(0);
    local_7a0[0] = CSelectColorWnd::vftable;
    this_00 = (WindowImplBase *)local_7a0;
    local_790 = CSelectColorWnd::vftable;
    local_780 = CSelectColorWnd::vftable;
    local_77c = CSelectColorWnd::vftable;
    local_778 = CSelectColorWnd::vftable;
    local_774 = CSelectColorWnd::vftable;
LAB_0040e434:
    DuiLib::WindowImplBase::~WindowImplBase(this_00);
  }
  else {
    iVar4 = 0;
    piVar3 = (int *)((int)this + 0x74);
    do {
      if (*(int *)(param_1 + 0x108) == *piVar3) {
        pCVar2 = DuiLib::CPaintManagerUI::FindControl
                           (*(CPaintManagerUI **)((int)this + 0x10),L"disable_window_ver");
        (**(code **)(*(int *)pCVar2 + 0xf8))(1,uVar1);
        memset(local_f2c,0,0x78c);
        DuiLib::WindowImplBase::WindowImplBase((WindowImplBase *)local_f2c);
        local_f2c[0] = CSelectColorWnd::vftable;
        local_f1c = CSelectColorWnd::vftable;
        local_f0c = CSelectColorWnd::vftable;
        local_f08 = CSelectColorWnd::vftable;
        local_f04 = CSelectColorWnd::vftable;
        local_f00 = CSelectColorWnd::vftable;
        local_7a8 = 0;
        local_8 = 1;
        uVar1 = *(uint *)(DAT_00432aa0 + 0x110 + iVar4 * 4);
        local_7a4 = (uint)*(byte *)(DAT_00432aa0 + 0x112 + iVar4 * 4) | (uVar1 | 0xffffff00) << 0x10
                    | uVar1 & 0xff00;
        DuiLib::CWindowWnd::Create
                  ((CWindowWnd *)local_f2c,*(HWND__ **)((int)this + 0x14),L"SelectColorWnd",
                   0x90000000,0x80,0,0,800,800,(HMENU__ *)0x0);
        DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_f2c);
        uVar1 = DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_f2c);
        if (uVar1 == 1) {
          DuiLib::CControlUI::SetBkColor(*(CControlUI **)((int)this + iVar4 * 4 + 0x74),local_7a4);
          *(uint *)(DAT_00432aa0 + 0x110 + iVar4 * 4) =
               ((local_7a4 & 0xff) << 8 | local_7a4 >> 8 & 0xff) << 8 | local_7a4 >> 0x10 & 0xff;
        }
        (**(code **)(*(int *)pCVar2 + 0xf8))(0);
        local_f2c[0] = CSelectColorWnd::vftable;
        this_00 = (WindowImplBase *)local_f2c;
        local_f1c = CSelectColorWnd::vftable;
        local_f0c = CSelectColorWnd::vftable;
        local_f08 = CSelectColorWnd::vftable;
        local_f04 = CSelectColorWnd::vftable;
        local_f00 = CSelectColorWnd::vftable;
        goto LAB_0040e434;
      }
      iVar4 = iVar4 + 1;
      piVar3 = piVar3 + 1;
    } while (iVar4 < 8);
  }
  ExceptionList = local_10;
  return;
}


