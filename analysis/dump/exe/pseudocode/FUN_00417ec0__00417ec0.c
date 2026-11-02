// Program: SM809 mouse Software.exe
// Function: FUN_00417ec0
// Entry: 00417ec0
// Body: 00417ec0 - 004181dc
// Signature: undefined FUN_00417ec0(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_00417ec0(int param_1)

{
  CResourceManager *this;
  CDuiString *pCVar1;
  CListLabelElementUI *pCVar2;
  wchar_t *_Src;
  CDuiString *this_00;
  CDuiString *this_01;
  code *pcVar3;
  CDuiString in_stack_fffffd3c;
  CDuiString aCStack_2c1 [101];
  wchar_t *pwVar4;
  wchar_t *local_22c;
  CListLabelElementUI *local_228;
  CDuiString local_224 [132];
  CDuiString local_1a0 [132];
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00423572;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  DuiLib::CDuiString::CDuiString(local_11c);
  pCVar1 = local_1a0;
  local_8 = 0;
  pwVar4 = L"profile_text";
  this = DuiLib::CResourceManager::GetInstance();
  pCVar1 = (CDuiString *)DuiLib::CResourceManager::GetText(this,(wchar_t *)pCVar1,pwVar4);
  local_8._0_1_ = 1;
  DuiLib::CDuiString::operator=(local_11c,pCVar1);
  local_8 = (uint)local_8._1_3_ << 8;
  DuiLib::CDuiString::~CDuiString(local_1a0);
  DuiLib::CDuiString::CDuiString(local_98);
  local_8._0_1_ = 2;
  DuiLib::CDuiString::GetData(local_11c);
  DuiLib::CDuiString::Format(this_00,(wchar_t *)local_98);
  DuiLib::CDuiString::operator=(local_11c,local_98);
  pwVar4 = operator_new(0x1cc50);
  local_22c = pwVar4;
  memset(pwVar4,0,0x1cc50);
  memcpy(pwVar4,&DAT_00432ae0,0x1cc50);
  DuiLib::CDuiString::CDuiString(aCStack_2c1 + -3,local_11c);
  local_228 = (CListLabelElementUI *)FUN_004039e0(in_stack_fffffd3c);
  if (local_228 == (CListLabelElementUI *)0x0) {
    pcVar3 = ~CDuiString_exref;
  }
  else {
    DuiLib::CDuiString::CDuiString(local_224);
    local_8._0_1_ = 3;
    DuiLib::CDuiString::CDuiString(local_1a0);
    local_8 = CONCAT31(local_8._1_3_,4);
    DuiLib::CDuiString::operator=(local_1a0,local_98);
    pCVar2 = local_228;
    while (pCVar2 == (CListLabelElementUI *)0x1) {
      DuiLib::CDuiString::GetData(local_98);
      DuiLib::CDuiString::Format(this_01,(wchar_t *)local_224);
      DuiLib::CDuiString::operator=(local_98,local_224);
      DuiLib::CDuiString::CDuiString(aCStack_2c1 + -3,local_98);
      pCVar2 = (CListLabelElementUI *)FUN_004039e0(in_stack_fffffd3c);
    }
    DuiLib::CDuiString::operator=(local_11c,local_98);
    pcVar3 = ~CDuiString_exref;
    DuiLib::CDuiString::~CDuiString(local_1a0);
    local_8._0_1_ = 2;
    DuiLib::CDuiString::~CDuiString(local_224);
    pwVar4 = local_22c;
  }
  DuiLib::CDuiString::operator=(local_98,local_11c);
  _Src = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
  wcscpy_s(pwVar4,0x32,_Src);
  if (DAT_0046c390 == DAT_0046c394) {
    FUN_00405390(DAT_0046c390,&local_22c);
  }
  else {
    *DAT_0046c390 = pwVar4;
    DAT_0046c390 = DAT_0046c390 + 1;
  }
  FUN_004035a0();
  DuiLib::CDuiString::CDuiString(local_1a0,pwVar4,-1);
  local_8._0_1_ = 5;
  pCVar2 = operator_new(0x570);
  local_8._0_1_ = 6;
  local_228 = pCVar2;
  DuiLib::CListLabelElementUI::CListLabelElementUI(pCVar2);
  *(undefined ***)pCVar2 = DuiLib::CListLabelElementUI::vftable;
  local_8._0_1_ = 5;
  pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_1a0);
  DuiLib::CControlUI::SetText((CControlUI *)pCVar2,pwVar4);
  (**(code **)(*(int *)pCVar2 + 0x88))();
  (**(code **)(*(int *)(*(int *)(param_1 + 0x16fc) + 0x558) + 0x10))();
  local_8 = CONCAT31(local_8._1_3_,2);
  (*pcVar3)();
  (**(code **)(*(int *)(*(int *)(param_1 + 0x16fc) + 0x6a0) + 0xc))();
  (*pcVar3)();
  (*pcVar3)();
  ExceptionList = local_10;
  return;
}


