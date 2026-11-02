// Program: SM809 mouse Software.exe
// Function: FUN_004014f0
// Entry: 004014f0
// Body: 004014f0 - 00401791
// Signature: undefined FUN_004014f0(void)


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_004014f0(void)

{
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_0042243e;
  local_10 = ExceptionList;
  ExceptionList = &local_10;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046d128,L"click",-1);
  local_8 = 0;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046d1ac,L"",-1);
  _DAT_0046d230 = 2;
  _DAT_0046d238 = &LAB_00408c5b;
  _DAT_0046d23c = 0;
  _DAT_0046d240 = 0;
  _DAT_0046d244 = 0;
  local_8 = 1;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046d248,L"selectchanged",-1);
  local_8._0_1_ = 2;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046d2cc,L"",-1);
  _DAT_0046d350 = 2;
  _DAT_0046d358 = &LAB_00408c60;
  _DAT_0046d35c = 0;
  _DAT_0046d360 = 0;
  _DAT_0046d364 = 0;
  local_8._0_1_ = 3;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046d368,L"valuechanged",-1);
  local_8._0_1_ = 4;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046d3ec,L"",-1);
  _DAT_0046d470 = 2;
  _DAT_0046d478 = &LAB_00408c51;
  _DAT_0046d47c = 0;
  _DAT_0046d480 = 0;
  _DAT_0046d484 = 0;
  local_8._0_1_ = 5;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046d488,L"colorchanged",-1);
  local_8._0_1_ = 6;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046d50c,L"",-1);
  _DAT_0046d590 = 2;
  _DAT_0046d598 = &LAB_00408c56;
  _DAT_0046d59c = 0;
  _DAT_0046d5a0 = 0;
  _DAT_0046d5a4 = 0;
  local_8._0_1_ = 7;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046d5a8,L"colorchangedbuttonup",-1);
  local_8._0_1_ = 8;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046d62c,L"",-1);
  _DAT_0046d6b0 = 2;
  _DAT_0046d6b8 = &LAB_0040de79;
  _DAT_0046d6bc = 0;
  _DAT_0046d6c0 = 0;
  _DAT_0046d6c4 = 0;
  local_8._0_1_ = 9;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046d6c8,L"textchanged",-1);
  local_8._0_1_ = 10;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046d74c,L"",-1);
  _DAT_0046d7d0 = 2;
  _DAT_0046d7d8 = &LAB_0040de7e;
  _DAT_0046d7dc = 0;
  _DAT_0046d7e0 = 0;
  _DAT_0046d7e4 = 0;
  local_8._0_1_ = 0xb;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046d7e8,L"",-1);
  local_8 = CONCAT31(local_8._1_3_,0xc);
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046d86c,L"",-1);
  _DAT_0046d8f0 = 0;
  _DAT_0046d8f8 = 0;
  _DAT_0046d8fc = 0;
  _DAT_0046d900 = 0;
  _DAT_0046d904 = 0xffffffff;
  _atexit((_func_4879 *)&LAB_00423c80);
  ExceptionList = local_10;
  return;
}


