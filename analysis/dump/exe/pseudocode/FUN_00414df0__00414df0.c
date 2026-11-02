// Program: SM809 mouse Software.exe
// Function: FUN_00414df0
// Entry: 00414df0
// Body: 00414df0 - 00414f97
// Signature: undefined FUN_00414df0(WindowImplBase * param_1)


void __fastcall FUN_00414df0(WindowImplBase *param_1)

{
  CNotifyPump *pCVar1;
  CDuiString aCStack_ac [124];
  undefined4 uStack_30;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 uStack_8;
  
  uStack_8 = 0xffffffff;
  puStack_c = &LAB_00422d70;
  local_10 = ExceptionList;
  ExceptionList = &local_10;
  pCVar1 = (CNotifyPump *)(param_1 + 0x10);
  *(undefined ***)param_1 = CMainWnd::vftable;
  *(undefined ***)pCVar1 = CMainWnd::vftable;
  *(undefined ***)(param_1 + 0x20) = CMainWnd::vftable;
  *(undefined ***)(param_1 + 0x24) = CMainWnd::vftable;
  *(undefined ***)(param_1 + 0x28) = CMainWnd::vftable;
  *(undefined ***)(param_1 + 0x2c) = CMainWnd::vftable;
  *(undefined ***)(param_1 + 0x764) = CMainWnd::vftable;
  DuiLib::CDuiString::CDuiString(aCStack_ac,L"ButtonPage",-1);
  DuiLib::CNotifyPump::RemoveVirtualWnd(pCVar1);
  DuiLib::CDuiString::CDuiString(aCStack_ac,L"PerformancePage",-1);
  DuiLib::CNotifyPump::RemoveVirtualWnd(pCVar1);
  DuiLib::CDuiString::CDuiString(aCStack_ac,L"LightPage",-1);
  DuiLib::CNotifyPump::RemoveVirtualWnd(pCVar1);
  DuiLib::CDuiString::CDuiString(aCStack_ac,L"MacroPage",-1);
  DuiLib::CNotifyPump::RemoveVirtualWnd(pCVar1);
  DuiLib::CDuiString::CDuiString(aCStack_ac,L"GunPage",-1);
  DuiLib::CNotifyPump::RemoveVirtualWnd(pCVar1);
  DuiLib::CTrayIcon::~CTrayIcon((CTrayIcon *)(param_1 + 0x1724));
  *(undefined ***)(param_1 + 0xef8) = CGunPage::vftable;
  DuiLib::CStdPtrArray::~CStdPtrArray((CStdPtrArray *)(param_1 + 0x1094));
  DuiLib::CStdPtrArray::~CStdPtrArray((CStdPtrArray *)(param_1 + 0x1088));
  DuiLib::CNotifyPump::~CNotifyPump((CNotifyPump *)(param_1 + 0xef8));
  *(undefined ***)(param_1 + 0xb40) = CMacroPage::vftable;
  if (*(HMODULE *)(param_1 + 0xe30) != (HMODULE)0x0) {
    uStack_30 = 0x414f1d;
    FreeLibrary(*(HMODULE *)(param_1 + 0xe30));
  }
  DuiLib::CStdPtrArray::~CStdPtrArray((CStdPtrArray *)(param_1 + 0xe44));
  DuiLib::CStdPtrArray::~CStdPtrArray((CStdPtrArray *)(param_1 + 0xe38));
  DuiLib::CNotifyPump::~CNotifyPump((CNotifyPump *)(param_1 + 0xb40));
  *(undefined ***)(param_1 + 0xa98) = CLightPage::vftable;
  DuiLib::CNotifyPump::~CNotifyPump((CNotifyPump *)(param_1 + 0xa98));
  *(undefined ***)(param_1 + 0x960) = CPerformancePage::vftable;
  DuiLib::CNotifyPump::~CNotifyPump((CNotifyPump *)(param_1 + 0x960));
  DuiLib::CNotifyPump::~CNotifyPump((CNotifyPump *)(param_1 + 0x7a0));
  *(undefined ***)(param_1 + 0x764) = ReceiverImpl<int,SkinChangedParam>::vftable;
  ~_Tree<>((int *)(param_1 + 0x768));
  DuiLib::WindowImplBase::~WindowImplBase(param_1);
  ExceptionList = local_10;
  return;
}


