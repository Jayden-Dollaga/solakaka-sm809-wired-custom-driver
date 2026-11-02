// Program: SM809 mouse Software.exe
// Function: FUN_00409140
// Entry: 00409140
// Body: 00409140 - 00409248
// Signature: undefined FUN_00409140(WindowImplBase * param_1)


void __fastcall FUN_00409140(WindowImplBase *param_1)

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
  *(undefined ***)param_1 = CEditGunName::vftable;
  *(undefined ***)(param_1 + 0x10) = CEditGunName::vftable;
  *(undefined ***)(param_1 + 0x20) = CEditGunName::vftable;
  *(undefined ***)(param_1 + 0x24) = CEditGunName::vftable;
  *(undefined ***)(param_1 + 0x28) = CEditGunName::vftable;
  *(undefined ***)(param_1 + 0x2c) = CEditGunName::vftable;
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
  *(undefined4 *)(param_1 + 0x870) = 0;
  ExceptionList = local_10;
  return;
}


