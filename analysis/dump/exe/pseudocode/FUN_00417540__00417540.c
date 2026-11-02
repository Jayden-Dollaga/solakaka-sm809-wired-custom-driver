// Program: SM809 mouse Software.exe
// Function: FUN_00417540
// Entry: 00417540
// Body: 00417540 - 004176eb
// Signature: undefined FUN_00417540(int param_1)


void __fastcall FUN_00417540(int param_1)

{
  int iVar1;
  
  FUN_00408bc0((void *)(param_1 + 0x7a0),*(int *)(DAT_00432aa0 + 0x14c));
  iVar1 = 0;
  do {
    FUN_004081e0((void *)(param_1 + 0x7a0),iVar1);
    iVar1 = iVar1 + 1;
  } while (iVar1 < 0x40);
  FUN_0041c7f0((void *)(param_1 + 0x960));
  (**(code **)(**(int **)(param_1 + 0xab4 + *(int *)(DAT_00432aa0 + 0xf0) * 4) + 0x1bc))(1,1);
  DuiLib::CSliderUI::SetValue(*(CSliderUI **)(param_1 + 0xaec),*(int *)(DAT_00432aa0 + 0xf4));
  DuiLib::CSliderUI::SetValue(*(CSliderUI **)(param_1 + 0xaf0),*(int *)(DAT_00432aa0 + 0xf8));
  DuiLib::CSliderUI::SetValue(*(CSliderUI **)(param_1 + 0xb3c),*(int *)(DAT_00432aa0 + 0x100));
  DuiLib::CControlUI::SetBkColor
            (*(CControlUI **)(param_1 + 0xaf4),
             (*(uint *)(DAT_00432aa0 + 0x104) | 0xffffff00) << 0x10 |
             (uint)*(byte *)(DAT_00432aa0 + 0x106) | *(uint *)(DAT_00432aa0 + 0x104) & 0xff00);
  DuiLib::CColorPaletteUI::SetSelectColor
            (*(CColorPaletteUI **)(param_1 + 0xaf8),
             (*(uint *)(DAT_00432aa0 + 0x104) | 0xffffff00) << 0x10 |
             (uint)*(byte *)(DAT_00432aa0 + 0x106) | *(uint *)(DAT_00432aa0 + 0x104) & 0xff00);
  FUN_0040e9c0((void *)(param_1 + 0xa98),*(uint *)(DAT_00432aa0 + 0x104));
  (**(code **)(**(int **)(param_1 + 0xb2c + *(int *)(DAT_00432aa0 + 0xfc) * 4) + 0x1bc))(1,1);
  DuiLib::CControlUI::SetBkColor
            (*(CControlUI **)(param_1 + 0xb08),
             (*(uint *)(DAT_00432aa0 + 0x104) | 0xffffff00) << 0x10 |
             (uint)*(byte *)(DAT_00432aa0 + 0x106) | *(uint *)(DAT_00432aa0 + 0x104) & 0xff00);
  iVar1 = 0x110;
  do {
    DuiLib::CControlUI::SetBkColor
              (*(CControlUI **)(param_1 + 0x9fc + iVar1),
               (uint)*(byte *)(iVar1 + 2 + DAT_00432aa0) |
               (*(uint *)(iVar1 + DAT_00432aa0) | 0xffffff00) << 0x10 |
               *(uint *)(iVar1 + DAT_00432aa0) & 0xff00);
    iVar1 = iVar1 + 4;
  } while (iVar1 < 0x130);
  FUN_0040eaf0((void *)(param_1 + 0xa98),*(int *)(DAT_00432aa0 + 0xf0));
  return;
}


