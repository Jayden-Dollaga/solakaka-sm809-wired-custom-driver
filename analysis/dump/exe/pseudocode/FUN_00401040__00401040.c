// Program: SM809 mouse Software.exe
// Function: FUN_00401040
// Entry: 00401040
// Body: 00401040 - 00401235
// Signature: undefined FUN_00401040(void)


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00401040(void)

{
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_004216a4;
  local_10 = ExceptionList;
  ExceptionList = &local_10;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046c3a8,L"click",-1);
  local_8 = 0;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046c42c,L"",-1);
  _DAT_0046c4b0 = 2;
  _DAT_0046c4b8 = &LAB_00408c5b;
  _DAT_0046c4bc = 0;
  _DAT_0046c4c0 = 0;
  _DAT_0046c4c4 = 0;
  local_8 = 1;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046c4c8,L"selectchanged",-1);
  local_8._0_1_ = 2;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046c54c,L"",-1);
  _DAT_0046c5d0 = 2;
  _DAT_0046c5d8 = &LAB_00408c60;
  _DAT_0046c5dc = 0;
  _DAT_0046c5e0 = 0;
  _DAT_0046c5e4 = 0;
  local_8._0_1_ = 3;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046c5e8,L"mouseenter",-1);
  local_8._0_1_ = 4;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046c66c,L"",-1);
  _DAT_0046c6f0 = 2;
  _DAT_0046c6f8 = &LAB_00408c51;
  _DAT_0046c6fc = 0;
  _DAT_0046c700 = 0;
  _DAT_0046c704 = 0;
  local_8._0_1_ = 5;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046c708,L"mouseleave",-1);
  local_8._0_1_ = 6;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046c78c,L"",-1);
  _DAT_0046c810 = 2;
  _DAT_0046c818 = &LAB_00408c56;
  _DAT_0046c81c = 0;
  _DAT_0046c820 = 0;
  _DAT_0046c824 = 0;
  local_8._0_1_ = 7;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046c828,L"",-1);
  local_8 = CONCAT31(local_8._1_3_,8);
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046c8ac,L"",-1);
  _DAT_0046c930 = 0;
  _DAT_0046c938 = 0;
  _DAT_0046c93c = 0;
  _DAT_0046c940 = 0;
  _DAT_0046c944 = 0xffffffff;
  _atexit((_func_4879 *)&LAB_00423c40);
  ExceptionList = local_10;
  return;
}


