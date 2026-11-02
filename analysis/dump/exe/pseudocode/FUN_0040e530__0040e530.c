// Program: SM809 mouse Software.exe
// Function: FUN_0040e530
// Entry: 0040e530
// Body: 0040e530 - 0040e57d
// Signature: undefined FUN_0040e530(void * this, int param_1)


void __thiscall FUN_0040e530(void *this,int param_1)

{
  ulong uVar1;
  
  if (*(CColorPaletteUI **)(param_1 + 0x108) == *(CColorPaletteUI **)((int)this + 0x60)) {
    uVar1 = DuiLib::CColorPaletteUI::GetSelectColor(*(CColorPaletteUI **)((int)this + 0x60));
    DuiLib::CControlUI::SetBkColor(*(CControlUI **)((int)this + 0x5c),uVar1);
    FUN_0040e9c0(this,((uVar1 & 0xff) << 8 | (uVar1 & 0xffff) >> 8) << 8 | uVar1 >> 0x10 & 0xff);
  }
  return;
}


