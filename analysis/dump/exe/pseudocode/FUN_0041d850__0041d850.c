// Program: SM809 mouse Software.exe
// Function: FUN_0041d850
// Entry: 0041d850
// Body: 0041d850 - 0041d941
// Signature: undefined FUN_0041d850(void * this, CDuiString * param_1)


void __thiscall FUN_0041d850(void *this,CDuiString *param_1)

{
  int iVar1;
  bool bVar2;
  ulong uVar3;
  
  bVar2 = DuiLib::CDuiString::operator==(param_1,L"click");
  if (bVar2) {
    iVar1 = *(int *)(param_1 + 0x108);
    if (iVar1 == *(int *)((int)this + 0x744)) {
      DuiLib::CWindowWnd::Close((CWindowWnd *)((int)this + -0x20),1);
      return;
    }
    if ((iVar1 == *(int *)((int)this + 0x748)) || (iVar1 == *(int *)((int)this + 0x74c))) {
      DuiLib::CWindowWnd::Close((CWindowWnd *)((int)this + -0x20),0);
      return;
    }
  }
  else {
    bVar2 = DuiLib::CDuiString::operator==(param_1,L"colorchanged");
    if (!bVar2) {
      bVar2 = DuiLib::CDuiString::operator==(param_1,L"textchanged");
      if (bVar2) {
        FUN_0041d950((void *)((int)this + -0x20),(int)param_1);
        return;
      }
      bVar2 = DuiLib::CDuiString::operator==(param_1,L"colorchangedbuttonup");
      if (!bVar2) {
        return;
      }
    }
    if (*(CColorPaletteUI **)(param_1 + 0x108) == *(CColorPaletteUI **)((int)this + 0x760)) {
      uVar3 = DuiLib::CColorPaletteUI::GetSelectColor(*(CColorPaletteUI **)((int)this + 0x760));
      *(ulong *)((int)this + 0x768) = uVar3;
      DuiLib::CControlUI::SetBkColor(*(CControlUI **)((int)this + 0x750),uVar3);
      FUN_0041dd40((void *)((int)this + -0x20),
                   ((uint)(*(ushort *)((int)this + 0x768) >> 8) |
                   (*(ushort *)((int)this + 0x768) & 0xff) << 8) << 8 |
                   (uint)*(byte *)((int)this + 0x76a));
    }
  }
  return;
}


