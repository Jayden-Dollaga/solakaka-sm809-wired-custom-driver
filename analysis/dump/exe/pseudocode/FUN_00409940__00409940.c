// Program: SM809 mouse Software.exe
// Function: FUN_00409940
// Entry: 00409940
// Body: 00409940 - 00409a3e
// Signature: WindowImplBase * FUN_00409940(WindowImplBase * param_1)


WindowImplBase * __fastcall FUN_00409940(WindowImplBase *param_1)

{
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00421a7a;
  local_10 = ExceptionList;
  ExceptionList = &local_10;
  DuiLib::WindowImplBase::WindowImplBase(param_1);
  local_8 = 0;
  *(undefined ***)param_1 = CEditMacroName::vftable;
  *(undefined ***)(param_1 + 0x10) = CEditMacroName::vftable;
  *(undefined ***)(param_1 + 0x20) = CEditMacroName::vftable;
  *(undefined ***)(param_1 + 0x24) = CEditMacroName::vftable;
  *(undefined ***)(param_1 + 0x28) = CEditMacroName::vftable;
  *(undefined ***)(param_1 + 0x2c) = CEditMacroName::vftable;
  DuiLib::CDuiString::CDuiString((CDuiString *)(param_1 + 0x768));
  local_8._0_1_ = 1;
  DuiLib::CDuiString::CDuiString((CDuiString *)(param_1 + 0x7ec));
  local_8._0_1_ = 2;
  DuiLib::CDuiString::CDuiString((CDuiString *)(param_1 + 0x874));
  local_8._0_1_ = 3;
  DuiLib::CDuiString::CDuiString((CDuiString *)(param_1 + 0x8f8));
  local_8 = CONCAT31(local_8._1_3_,4);
  *(undefined4 *)(param_1 + 0x97c) = 0;
  *(undefined4 *)(param_1 + 0x870) = 0;
  DuiLib::CDuiString::operator=((CDuiString *)(param_1 + 0x768),L"");
  DuiLib::CDuiString::operator=((CDuiString *)(param_1 + 0x7ec),L"");
  DuiLib::CDuiString::operator=((CDuiString *)(param_1 + 0x874),L"");
  DuiLib::CDuiString::operator=((CDuiString *)(param_1 + 0x8f8),L"");
  ExceptionList = local_10;
  return param_1;
}


