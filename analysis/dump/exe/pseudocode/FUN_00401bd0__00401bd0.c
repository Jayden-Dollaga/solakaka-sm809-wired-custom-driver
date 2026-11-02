// Program: SM809 mouse Software.exe
// Function: FUN_00401bd0
// Entry: 00401bd0
// Body: 00401bd0 - 00401e71
// Signature: undefined FUN_00401bd0(void)


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00401bd0(void)

{
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_0042382e;
  local_10 = ExceptionList;
  ExceptionList = &local_10;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046e568,L"click",-1);
  local_8 = 0;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046e5ec,L"",-1);
  _DAT_0046e670 = 2;
  _DAT_0046e678 = &LAB_00408c5b;
  _DAT_0046e67c = 0;
  _DAT_0046e680 = 0;
  _DAT_0046e684 = 0;
  local_8 = 1;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046e688,L"selectchanged",-1);
  local_8._0_1_ = 2;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046e70c,L"",-1);
  _DAT_0046e790 = 2;
  _DAT_0046e798 = &LAB_00408c60;
  _DAT_0046e79c = 0;
  _DAT_0046e7a0 = 0;
  _DAT_0046e7a4 = 0;
  local_8._0_1_ = 3;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046e7a8,L"valuechanged",-1);
  local_8._0_1_ = 4;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046e82c,L"",-1);
  _DAT_0046e8b0 = 2;
  _DAT_0046e8b8 = &LAB_00408c51;
  _DAT_0046e8bc = 0;
  _DAT_0046e8c0 = 0;
  _DAT_0046e8c4 = 0;
  local_8._0_1_ = 5;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046e8c8,L"movevaluechanged",-1);
  local_8._0_1_ = 6;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046e94c,L"",-1);
  _DAT_0046e9d0 = 2;
  _DAT_0046e9d8 = &LAB_00408c56;
  _DAT_0046e9dc = 0;
  _DAT_0046e9e0 = 0;
  _DAT_0046e9e4 = 0;
  local_8._0_1_ = 7;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046e9e8,L"checkclick",-1);
  local_8._0_1_ = 8;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046ea6c,L"",-1);
  _DAT_0046eaf0 = 2;
  _DAT_0046eaf8 = &LAB_0040de79;
  _DAT_0046eafc = 0;
  _DAT_0046eb00 = 0;
  _DAT_0046eb04 = 0;
  local_8._0_1_ = 9;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046eb08,L"itemselect",-1);
  local_8._0_1_ = 10;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046eb8c,L"",-1);
  _DAT_0046ec10 = 2;
  _DAT_0046ec18 = &LAB_0040de7e;
  _DAT_0046ec1c = 0;
  _DAT_0046ec20 = 0;
  _DAT_0046ec24 = 0;
  local_8._0_1_ = 0xb;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046ec28,L"",-1);
  local_8 = CONCAT31(local_8._1_3_,0xc);
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046ecac,L"",-1);
  _DAT_0046ed30 = 0;
  _DAT_0046ed38 = 0;
  _DAT_0046ed3c = 0;
  _DAT_0046ed40 = 0;
  _DAT_0046ed44 = 0xffffffff;
  _atexit((_func_4879 *)&LAB_00423de0);
  ExceptionList = local_10;
  return;
}


