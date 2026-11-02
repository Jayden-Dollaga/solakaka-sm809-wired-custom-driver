// Program: SM809 mouse Software.exe
// Function: FUN_0041cad0
// Entry: 0041cad0
// Body: 0041cad0 - 0041ccc9
// Signature: undefined FUN_0041cad0(void * this, int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_0041cad0(void *this,int param_1)

{
  uint uVar1;
  int *piVar2;
  CControlUI *pCVar3;
  int iVar4;
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
  puStack_c = &LAB_004238f0;
  local_10 = ExceptionList;
  uVar1 = DAT_00432008 ^ (int)register0x00000010 - 4U;
  iVar4 = 0;
  piVar2 = (int *)((int)this + 0xe8);
  do {
    if (*(int *)(param_1 + 0x108) == *piVar2) {
      ExceptionList = &local_10;
      local_14 = uVar1;
      pCVar3 = DuiLib::CPaintManagerUI::FindControl
                         (*(CPaintManagerUI **)((int)this + 0x10),L"disable_window_ver");
      (**(code **)(*(int *)pCVar3 + 0xf8))(1,uVar1);
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
      uVar1 = *(uint *)(DAT_00432aa0 + 0xd0 + iVar4 * 4);
      local_18 = (uint)*(byte *)(DAT_00432aa0 + 0xd2 + iVar4 * 4) | (uVar1 | 0xffffff00) << 0x10 |
                 uVar1 & 0xff00;
      DuiLib::CWindowWnd::Create
                ((CWindowWnd *)local_7a0,*(HWND__ **)((int)this + 0x14),L"SelectColorWnd",0x90000000
                 ,0x80,0,0,800,800,(HMENU__ *)0x0);
      DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_7a0);
      uVar1 = DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_7a0);
      if (uVar1 == 1) {
        DuiLib::CControlUI::SetBkColor(*(CControlUI **)((int)this + iVar4 * 4 + 0xe8),local_18);
        *(uint *)(DAT_00432aa0 + 0xd0 + iVar4 * 4) =
             ((local_18 & 0xff) << 8 | local_18 >> 8 & 0xff) << 8 | local_18 >> 0x10 & 0xff;
      }
      (**(code **)(*(int *)pCVar3 + 0xf8))(0);
      local_7a0[0] = CSelectColorWnd::vftable;
      local_790 = CSelectColorWnd::vftable;
      local_780 = CSelectColorWnd::vftable;
      local_77c = CSelectColorWnd::vftable;
      local_778 = CSelectColorWnd::vftable;
      local_774 = CSelectColorWnd::vftable;
      DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_7a0);
      ExceptionList = local_10;
      return;
    }
    iVar4 = iVar4 + 1;
    piVar2 = piVar2 + 1;
  } while (iVar4 < 8);
  return;
}


