// Program: SM809 mouse Software.exe
// Function: FUN_0041f990
// Entry: 0041f990
// Body: 0041f990 - 0041fb30
// Signature: undefined4 FUN_0041f990(void * this, int param_1, UINT param_2, undefined4 param_3, undefined4 * param_4)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

undefined4 __thiscall
FUN_0041f990(void *this,int param_1,UINT param_2,undefined4 param_3,undefined4 *param_4)

{
  int iVar1;
  CDuiString *pCVar2;
  wchar_t *pwVar3;
  CResourceManager *this_00;
  CDuiString local_1ac [132];
  undefined4 *local_128;
  int local_124;
  void *local_120;
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00423bf5;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  local_128 = param_4;
  *param_4 = 1;
  local_120 = this;
  if (param_1 == 2) {
    (**(code **)((int)this + 0x774))(local_14);
  }
  else if (param_1 == 0x500) {
    DuiLib::DUI__Trace(L"%x,%x\n",param_2,param_3);
    DuiLib::CDuiString::CDuiString(local_11c);
    local_8 = 0;
    FUN_004022f0(param_2,&local_124);
    DuiLib::DUI__Trace(L"iUsageID=%d\n",local_124);
    *(char *)((int)local_120 + 0x7a8) = (char)local_124;
    DuiLib::CDuiString::CDuiString(local_98);
    local_8._0_1_ = 1;
    pCVar2 = FUN_00402370(local_1ac,local_124);
    local_8._0_1_ = 2;
    DuiLib::CDuiString::operator=(local_98,pCVar2);
    local_8._0_1_ = 1;
    DuiLib::CDuiString::~CDuiString(local_1ac);
    pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    pCVar2 = local_1ac;
    this_00 = DuiLib::CResourceManager::GetInstance();
    pCVar2 = (CDuiString *)DuiLib::CResourceManager::GetText(this_00,(wchar_t *)pCVar2,pwVar3);
    local_8._0_1_ = 3;
    DuiLib::CDuiString::operator=(local_98,pCVar2);
    local_8 = CONCAT31(local_8._1_3_,1);
    DuiLib::CDuiString::~CDuiString(local_1ac);
    iVar1 = **(int **)((int)local_120 + 0x798);
    pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    (**(code **)(iVar1 + 0x2c))(pwVar3);
    DuiLib::CDuiString::~CDuiString(local_98);
    DuiLib::CDuiString::~CDuiString(local_11c);
    *local_128 = 0;
    ExceptionList = local_10;
    return 0;
  }
  *param_4 = 0;
  ExceptionList = local_10;
  return 0;
}


