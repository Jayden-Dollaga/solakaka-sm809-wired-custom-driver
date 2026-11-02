// Program: SM809 mouse Software.exe
// Function: FUN_0041c1c0
// Entry: 0041c1c0
// Body: 0041c1c0 - 0041c27d
// Signature: WindowImplBase * FUN_0041c1c0(WindowImplBase * param_1)


WindowImplBase * __fastcall FUN_0041c1c0(WindowImplBase *param_1)

{
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_0042377c;
  local_10 = ExceptionList;
  ExceptionList = &local_10;
  DuiLib::WindowImplBase::WindowImplBase(param_1);
  local_8 = 0;
  *(undefined ***)param_1 = CMsgWnd::vftable;
  *(undefined ***)(param_1 + 0x10) = CMsgWnd::vftable;
  *(undefined ***)(param_1 + 0x20) = CMsgWnd::vftable;
  *(undefined ***)(param_1 + 0x24) = CMsgWnd::vftable;
  *(undefined ***)(param_1 + 0x28) = CMsgWnd::vftable;
  *(undefined ***)(param_1 + 0x2c) = CMsgWnd::vftable;
  DuiLib::CDuiString::CDuiString((CDuiString *)(param_1 + 0x77c));
  local_8._0_1_ = 1;
  DuiLib::CDuiString::CDuiString((CDuiString *)(param_1 + 0x800));
  local_8 = CONCAT31(local_8._1_3_,2);
  param_1[0x778] = (WindowImplBase)0x0;
  DuiLib::CDuiString::operator=((CDuiString *)(param_1 + 0x77c),L"");
  DuiLib::CDuiString::operator=((CDuiString *)(param_1 + 0x800),L"");
  ExceptionList = local_10;
  return param_1;
}


