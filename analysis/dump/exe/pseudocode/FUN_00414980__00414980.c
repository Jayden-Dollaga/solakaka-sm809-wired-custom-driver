// Program: SM809 mouse Software.exe
// Function: FUN_00414980
// Entry: 00414980
// Body: 00414980 - 00414da4
// Signature: WindowImplBase * FUN_00414980(WindowImplBase * param_1)


WindowImplBase * __fastcall FUN_00414980(WindowImplBase *param_1)

{
  void *pvVar1;
  CDuiString aCStack_b0 [120];
  undefined4 uStack_38;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00422d4f;
  local_10 = ExceptionList;
  ExceptionList = &local_10;
  DuiLib::WindowImplBase::WindowImplBase(param_1);
  local_8 = 0;
  *(undefined ***)(param_1 + 0x764) = ReceiverImpl<int,SkinChangedParam>::vftable;
  *(undefined4 *)(param_1 + 0x768) = 0;
  *(undefined4 *)(param_1 + 0x76c) = 0;
  pvVar1 = operator_new(0x18);
  *(void **)pvVar1 = pvVar1;
  *(void **)((int)pvVar1 + 4) = pvVar1;
  *(void **)((int)pvVar1 + 8) = pvVar1;
  *(undefined2 *)((int)pvVar1 + 0xc) = 0x101;
  *(void **)(param_1 + 0x768) = pvVar1;
  *(undefined4 *)(param_1 + 0x770) = 0;
  local_8._0_1_ = 1;
  *(undefined ***)param_1 = CMainWnd::vftable;
  *(undefined ***)(param_1 + 0x10) = CMainWnd::vftable;
  *(undefined ***)(param_1 + 0x20) = CMainWnd::vftable;
  *(undefined ***)(param_1 + 0x24) = CMainWnd::vftable;
  *(undefined ***)(param_1 + 0x28) = CMainWnd::vftable;
  *(undefined ***)(param_1 + 0x2c) = CMainWnd::vftable;
  *(undefined ***)(param_1 + 0x764) = CMainWnd::vftable;
  DuiLib::CNotifyPump::CNotifyPump((CNotifyPump *)(param_1 + 0x7a0));
  *(undefined ***)(param_1 + 0x7a0) = CButtonPage::vftable;
  *(undefined4 *)(param_1 + 0x7b0) = 0;
  *(undefined4 *)(param_1 + 0x7b4) = 0;
  *(undefined4 *)(param_1 + 0x7b8) = 0xffffffff;
  *(undefined4 *)(param_1 + 0x7bc) = 0;
  local_8._0_1_ = 2;
  DuiLib::CNotifyPump::CNotifyPump((CNotifyPump *)(param_1 + 0x960));
  *(undefined ***)(param_1 + 0x960) = CPerformancePage::vftable;
  *(undefined4 *)(param_1 + 0x970) = 0;
  *(undefined4 *)(param_1 + 0x974) = 0;
  local_8._0_1_ = 3;
  DuiLib::CNotifyPump::CNotifyPump((CNotifyPump *)(param_1 + 0xa98));
  *(undefined ***)(param_1 + 0xa98) = CLightPage::vftable;
  *(undefined4 *)(param_1 + 0xaa8) = 0;
  *(undefined4 *)(param_1 + 0xaac) = 0;
  *(undefined4 *)(param_1 + 0xab0) = 0xffffffff;
  local_8._0_1_ = 4;
  DuiLib::CNotifyPump::CNotifyPump((CNotifyPump *)(param_1 + 0xb40));
  local_8._0_1_ = 5;
  *(undefined ***)(param_1 + 0xb40) = CMacroPage::vftable;
  DuiLib::CStdPtrArray::CStdPtrArray((CStdPtrArray *)(param_1 + 0xe38),0);
  local_8._0_1_ = 6;
  DuiLib::CStdPtrArray::CStdPtrArray((CStdPtrArray *)(param_1 + 0xe44),0);
  local_8._0_1_ = 7;
  *(undefined4 *)(param_1 + 0xe30) = 0;
  *(undefined4 *)(param_1 + 0xb50) = 0;
  *(undefined4 *)(param_1 + 0xb54) = 0;
  *(undefined4 *)(param_1 + 0xb5c) = 0;
  *(undefined4 *)(param_1 + 0xb60) = 1;
  uStack_38 = 0x414b3f;
  memset(param_1 + 0xb64,0,0x280);
  *(undefined4 *)(param_1 + 0xde4) = 0;
  *(undefined2 *)(param_1 + 0xdf8) = 10;
  *(undefined4 *)(param_1 + 0xdf0) = 0xffffffff;
  *(undefined4 *)(param_1 + 0xdf4) = 0xffffffff;
  *(undefined4 *)(param_1 + 0xde8) = 0;
  *(undefined4 *)(param_1 + 0xdec) = 0;
  *(undefined4 *)(param_1 + 0xdfc) = 0xffffffff;
  *(undefined4 *)(param_1 + 0xe00) = 0;
  *(undefined4 *)(param_1 + 0xe08) = 0;
  *(undefined2 *)(param_1 + 0xe04) = 0;
  *(undefined4 *)(param_1 + 0xe2c) = 0;
  *(undefined4 *)(param_1 + 0xb58) = 0;
  *(undefined4 *)(param_1 + 0xe34) = 1;
  DuiLib::CStdPtrArray::Empty((CStdPtrArray *)(param_1 + 0xe38));
  DuiLib::CStdPtrArray::Empty((CStdPtrArray *)(param_1 + 0xe44));
  *(undefined4 *)(param_1 + 0xe50) = 0xffffffff;
  *(undefined4 *)(param_1 + 0xe54) = 0xffffffff;
  local_8._0_1_ = 8;
  DuiLib::CNotifyPump::CNotifyPump((CNotifyPump *)(param_1 + 0xef8));
  local_8._0_1_ = 9;
  *(undefined ***)(param_1 + 0xef8) = CGunPage::vftable;
  DuiLib::CStdPtrArray::CStdPtrArray((CStdPtrArray *)(param_1 + 0x1088),0);
  local_8._0_1_ = 10;
  DuiLib::CStdPtrArray::CStdPtrArray((CStdPtrArray *)(param_1 + 0x1094),0);
  local_8._0_1_ = 0xb;
  *(undefined4 *)(param_1 + 0xf14) = 0;
  *(undefined4 *)(param_1 + 0xf18) = 0x1e;
  *(undefined4 *)(param_1 + 0xf1c) = 0;
  *(undefined4 *)(param_1 + 0xf10) = 0;
  DuiLib::CStdPtrArray::Empty((CStdPtrArray *)(param_1 + 0x1088));
  DuiLib::CStdPtrArray::Empty((CStdPtrArray *)(param_1 + 0x1094));
  *(undefined4 *)(param_1 + 0x10a0) = 0xffffffff;
  *(undefined4 *)(param_1 + 0x10a4) = 0xffffffff;
  local_8._0_1_ = 0xc;
  DuiLib::CTrayIcon::CTrayIcon((CTrayIcon *)(param_1 + 0x1724));
  local_8 = CONCAT31(local_8._1_3_,0xd);
  *(undefined4 *)(param_1 + 0x1580) = 0;
  *(undefined4 *)(param_1 + 0x1720) = 0;
  *(undefined4 *)(param_1 + 0x1af0) = 0;
  DAT_00432ac4 = 0;
  DAT_00432ac0 = 0;
  *(undefined4 *)(param_1 + 0x16d0) = 0;
  uStack_38 = 0x414ce5;
  memset(param_1 + 0x1588,0,0x148);
  DuiLib::CDuiString::CDuiString(aCStack_b0,L"ButtonPage",-1);
  DuiLib::CNotifyPump::AddVirtualWnd((CNotifyPump *)(param_1 + 0x10));
  DuiLib::CDuiString::CDuiString(aCStack_b0,L"PerformancePage",-1);
  DuiLib::CNotifyPump::AddVirtualWnd((CNotifyPump *)(param_1 + 0x10));
  DuiLib::CDuiString::CDuiString(aCStack_b0,L"LightPage",-1);
  DuiLib::CNotifyPump::AddVirtualWnd((CNotifyPump *)(param_1 + 0x10));
  DuiLib::CDuiString::CDuiString(aCStack_b0,L"MacroPage",-1);
  DuiLib::CNotifyPump::AddVirtualWnd((CNotifyPump *)(param_1 + 0x10));
  DuiLib::CDuiString::CDuiString(aCStack_b0,L"GunPage",-1);
  DuiLib::CNotifyPump::AddVirtualWnd((CNotifyPump *)(param_1 + 0x10));
  ExceptionList = local_10;
  return param_1;
}


