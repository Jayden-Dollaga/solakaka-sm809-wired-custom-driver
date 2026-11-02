// Program: SM809 mouse Software.exe
// Function: FUN_0041d770
// Entry: 0041d770
// Body: 0041d770 - 0041d846
// Signature: undefined FUN_0041d770(void * param_1)


void __fastcall FUN_0041d770(void *param_1)

{
  CControlUI *pCVar1;
  
  pCVar1 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)((int)param_1 + 0x30),L"ok_btn");
  *(CControlUI **)((int)param_1 + 0x764) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     ((CPaintManagerUI *)((int)param_1 + 0x30),L"cancel_btn");
  *(CControlUI **)((int)param_1 + 0x768) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     ((CPaintManagerUI *)((int)param_1 + 0x30),L"exit_btn");
  *(CControlUI **)((int)param_1 + 0x76c) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     ((CPaintManagerUI *)((int)param_1 + 0x30),L"current_color_control");
  *(CControlUI **)((int)param_1 + 0x770) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)((int)param_1 + 0x30),L"r_edit");
  *(CControlUI **)((int)param_1 + 0x774) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)((int)param_1 + 0x30),L"g_edit");
  *(CControlUI **)((int)param_1 + 0x778) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)((int)param_1 + 0x30),L"b_edit");
  *(CControlUI **)((int)param_1 + 0x77c) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl
                     ((CPaintManagerUI *)((int)param_1 + 0x30),L"color_Pallet");
  *(CControlUI **)((int)param_1 + 0x780) = pCVar1;
  DuiLib::CColorPaletteUI::SetSelectColor
            ((CColorPaletteUI *)pCVar1,*(ulong *)((int)param_1 + 0x788));
  DuiLib::CControlUI::SetBkColor
            (*(CControlUI **)((int)param_1 + 0x770),*(ulong *)((int)param_1 + 0x788));
  FUN_0041dd40(param_1,((uint)(*(ushort *)((int)param_1 + 0x788) >> 8) |
                       (*(ushort *)((int)param_1 + 0x788) & 0xff) << 8) << 8 |
                       (uint)*(byte *)((int)param_1 + 0x78a));
  return;
}


