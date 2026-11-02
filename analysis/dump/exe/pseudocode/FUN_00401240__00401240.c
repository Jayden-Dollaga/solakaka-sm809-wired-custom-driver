// Program: SM809 mouse Software.exe
// Function: FUN_00401240
// Entry: 00401240
// Body: 00401240 - 004014e1
// Signature: undefined FUN_00401240(void)


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00401240(void)

{
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00421bfe;
  local_10 = ExceptionList;
  ExceptionList = &local_10;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046c948,L"click",-1);
  local_8 = 0;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046c9cc,L"",-1);
  _DAT_0046ca50 = 2;
  _DAT_0046ca58 = &LAB_00408c5b;
  _DAT_0046ca5c = 0;
  _DAT_0046ca60 = 0;
  _DAT_0046ca64 = 0;
  local_8 = 1;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046ca68,L"selectchanged",-1);
  local_8._0_1_ = 2;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046caec,L"",-1);
  _DAT_0046cb70 = 2;
  _DAT_0046cb78 = &LAB_00408c60;
  _DAT_0046cb7c = 0;
  _DAT_0046cb80 = 0;
  _DAT_0046cb84 = 0;
  local_8._0_1_ = 3;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046cb88,L"itemselect",-1);
  local_8._0_1_ = 4;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046cc0c,L"",-1);
  _DAT_0046cc90 = 2;
  _DAT_0046cc98 = &LAB_00408c51;
  _DAT_0046cc9c = 0;
  _DAT_0046cca0 = 0;
  _DAT_0046cca4 = 0;
  local_8._0_1_ = 5;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046cca8,L"checkclick",-1);
  local_8._0_1_ = 6;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046cd2c,L"",-1);
  _DAT_0046cdb0 = 2;
  _DAT_0046cdb8 = &LAB_00408c56;
  _DAT_0046cdbc = 0;
  _DAT_0046cdc0 = 0;
  _DAT_0046cdc4 = 0;
  local_8._0_1_ = 7;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046cdc8,L"killfocus",-1);
  local_8._0_1_ = 8;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046ce4c,L"",-1);
  _DAT_0046ced0 = 2;
  _DAT_0046ced8 = &LAB_0040de79;
  _DAT_0046cedc = 0;
  _DAT_0046cee0 = 0;
  _DAT_0046cee4 = 0;
  local_8._0_1_ = 9;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046cee8,L"textchanged",-1);
  local_8._0_1_ = 10;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046cf6c,L"",-1);
  _DAT_0046cff0 = 2;
  _DAT_0046cff8 = &LAB_0040de7e;
  _DAT_0046cffc = 0;
  _DAT_0046d000 = 0;
  _DAT_0046d004 = 0;
  local_8._0_1_ = 0xb;
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046d008,L"",-1);
  local_8 = CONCAT31(local_8._1_3_,0xc);
  DuiLib::CDuiString::CDuiString((CDuiString *)&DAT_0046d08c,L"",-1);
  _DAT_0046d110 = 0;
  _DAT_0046d118 = 0;
  _DAT_0046d11c = 0;
  _DAT_0046d120 = 0;
  _DAT_0046d124 = 0xffffffff;
  _atexit((_func_4879 *)&LAB_00423c60);
  ExceptionList = local_10;
  return;
}


