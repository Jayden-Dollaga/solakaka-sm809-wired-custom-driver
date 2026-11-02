// Program: SM809 mouse Software.exe
// Function: FUN_00403af0
// Entry: 00403af0
// Body: 00403af0 - 00403d6a
// Signature: wchar_t * FUN_00403af0(undefined4 param_1, int param_2)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

wchar_t * __fastcall FUN_00403af0(undefined4 param_1,int param_2)

{
  CResourceManager *this;
  CDuiString *pCVar1;
  int iVar2;
  wchar_t *_Src;
  CDuiString *this_00;
  CDuiString *this_01;
  code *pcVar3;
  CDuiString in_stack_fffffd30;
  CDuiString aCStack_2cd [113];
  wchar_t *pwVar4;
  wchar_t *local_238;
  CDuiString local_234 [136];
  CDuiString local_1ac [136];
  CDuiString local_124 [136];
  CDuiString local_9c [136];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00421351;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_9c + 0x98);
  ExceptionList = &local_10;
  DuiLib::CDuiString::CDuiString(local_124);
  pCVar1 = local_1ac;
  local_8 = 0;
  pwVar4 = L"profile_text";
  this = DuiLib::CResourceManager::GetInstance();
  pCVar1 = (CDuiString *)DuiLib::CResourceManager::GetText(this,(wchar_t *)pCVar1,pwVar4);
  local_8._0_1_ = 1;
  DuiLib::CDuiString::operator=(local_124,pCVar1);
  local_8 = (uint)local_8._1_3_ << 8;
  DuiLib::CDuiString::~CDuiString(local_1ac);
  DuiLib::CDuiString::CDuiString(local_9c);
  local_8._0_1_ = 2;
  DuiLib::CDuiString::GetData(local_124);
  DuiLib::CDuiString::Format(this_00,(wchar_t *)local_9c);
  DuiLib::CDuiString::operator=(local_124,local_9c);
  pwVar4 = operator_new(0x1cc50);
  local_238 = pwVar4;
  memset(pwVar4,0,0x1cc50);
  FUN_004020d0((int)pwVar4,param_2);
  DuiLib::CDuiString::CDuiString(aCStack_2cd + -3,local_124);
  iVar2 = FUN_004039e0(in_stack_fffffd30);
  if (iVar2 == 0) {
    pcVar3 = ~CDuiString_exref;
  }
  else {
    DuiLib::CDuiString::CDuiString(local_234);
    local_8._0_1_ = 3;
    DuiLib::CDuiString::CDuiString(local_1ac);
    local_8 = CONCAT31(local_8._1_3_,4);
    DuiLib::CDuiString::operator=(local_1ac,local_9c);
    while (iVar2 == 1) {
      DuiLib::CDuiString::GetData(local_9c);
      DuiLib::CDuiString::Format(this_01,(wchar_t *)local_234);
      DuiLib::CDuiString::operator=(local_9c,local_234);
      DuiLib::CDuiString::CDuiString(aCStack_2cd + -3,local_9c);
      iVar2 = FUN_004039e0(in_stack_fffffd30);
    }
    DuiLib::CDuiString::operator=(local_124,local_9c);
    pcVar3 = ~CDuiString_exref;
    DuiLib::CDuiString::~CDuiString(local_1ac);
    local_8._0_1_ = 2;
    DuiLib::CDuiString::~CDuiString(local_234);
  }
  DuiLib::CDuiString::operator=(local_9c,local_124);
  _Src = DuiLib::CDuiString::operator_wchar_t_const_(local_9c);
  pwVar4 = local_238;
  wcscpy_s(local_238,0x32,_Src);
  if (DAT_0046c390 == DAT_0046c394) {
    FUN_00405390(DAT_0046c390,&local_238);
  }
  else {
    *DAT_0046c390 = pwVar4;
    DAT_0046c390 = DAT_0046c390 + 1;
  }
  FUN_004035a0();
  (*pcVar3)();
  (*pcVar3)();
  ExceptionList = local_10;
  return pwVar4;
}


