// Program: SM809 mouse Software.exe
// Function: FUN_0041e490
// Entry: 0041e490
// Body: 0041e490 - 0041e673
// Signature: undefined FUN_0041e490(void * this, int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_0041e490(void *this,int param_1)

{
  int iVar1;
  uint uVar2;
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
  puStack_c = &LAB_00423a80;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (int)register0x00000010 - 4U;
  iVar1 = *(int *)(param_1 + 0x108);
  if (iVar1 == *(int *)((int)this + 0x764)) {
    uVar2 = 1;
  }
  else {
    if ((iVar1 != *(int *)((int)this + 0x768)) && (iVar1 != *(int *)((int)this + 0x76c))) {
      if (iVar1 != *(int *)((int)this + 0x780)) {
        return;
      }
      ExceptionList = &local_10;
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
      uVar2 = *(uint *)((int)this + 0x78c);
      local_18 = uVar2 >> 0x10 & 0xff | (uVar2 | 0xffffff00) << 0x10 | uVar2 & 0xff00;
      DuiLib::CWindowWnd::Create
                ((CWindowWnd *)local_7a0,*(HWND__ **)((int)this + 4),L"SelectColorWnd",0x90000000,
                 0x80,0,0,800,800,(HMENU__ *)0x0);
      DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_7a0);
      uVar2 = DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_7a0);
      if (uVar2 == 1) {
        DuiLib::CControlUI::SetBkColor(*(CControlUI **)((int)this + 0x780),local_18);
        *(uint *)((int)this + 0x78c) =
             ((local_18 & 0xff) << 8 | local_18 >> 8 & 0xff) << 8 | local_18 >> 0x10 & 0xff;
      }
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
    uVar2 = 0;
  }
  ExceptionList = &local_10;
  DuiLib::CWindowWnd::Close(this,uVar2);
  ExceptionList = local_10;
  return;
}


