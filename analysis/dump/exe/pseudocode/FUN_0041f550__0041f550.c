// Program: SM809 mouse Software.exe
// Function: FUN_0041f550
// Entry: 0041f550
// Body: 0041f550 - 0041f847
// Signature: undefined FUN_0041f550(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_0041f550(int param_1)

{
  CPaintManagerUI *this;
  CControlUI *pCVar1;
  wchar_t *pwVar2;
  CDuiString *pCVar3;
  CResourceManager *this_00;
  HMODULE hModule;
  DWORD DVar4;
  FARPROC pFVar5;
  CDuiString *extraout_ECX;
  CDuiString *extraout_ECX_00;
  CDuiString *this_01;
  undefined4 *puVar6;
  int iVar7;
  int iVar8;
  CDuiString local_230 [132];
  int local_1ac;
  int local_1a8;
  CPaintManagerUI *local_1a4;
  CDuiString local_1a0 [132];
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00423b89;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  this = (CPaintManagerUI *)(param_1 + 0x30);
  local_1ac = param_1;
  local_1a4 = this;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl(this,L"ok_btn");
  *(CControlUI **)(param_1 + 0x77c) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl(this,L"cancel_btn");
  *(CControlUI **)(param_1 + 0x780) = pCVar1;
  pCVar1 = DuiLib::CPaintManagerUI::FindControl(this,L"exit_btn");
  *(CControlUI **)(param_1 + 0x784) = pCVar1;
  DuiLib::CDuiString::CDuiString(local_11c);
  iVar8 = 1;
  local_8 = 0;
  local_1a8 = param_1 + 0x7a3;
  puVar6 = (undefined4 *)(param_1 + 0x788);
  iVar7 = 4;
  pCVar3 = extraout_ECX;
  do {
    DuiLib::CDuiString::Format(pCVar3,(wchar_t *)local_11c,L"check_flag_%d",iVar8);
    pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_11c);
    pCVar1 = DuiLib::CPaintManagerUI::FindControl(local_1a4,pwVar2);
    *puVar6 = pCVar1;
    DuiLib::CCheckBoxUI::SetCheck((CCheckBoxUI *)pCVar1,*(char *)(local_1a8 + iVar8) != '\0');
    iVar8 = iVar8 + 1;
    puVar6 = puVar6 + 1;
    iVar7 = iVar7 + -1;
    pCVar3 = extraout_ECX_00;
  } while (iVar7 != 0);
  pCVar1 = DuiLib::CPaintManagerUI::FindControl(local_1a4,L"edit_key");
  iVar8 = local_1ac;
  *(CControlUI **)(local_1ac + 0x798) = pCVar1;
  pCVar3 = FUN_00402370(local_98,(uint)*(byte *)(local_1ac + 0x7a8));
  local_8._0_1_ = 1;
  DuiLib::CDuiString::operator=(local_11c,pCVar3);
  local_8 = (uint)local_8._1_3_ << 8;
  DuiLib::CDuiString::~CDuiString(local_98);
  pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_11c);
  pCVar3 = local_98;
  this_00 = DuiLib::CResourceManager::GetInstance();
  pCVar3 = (CDuiString *)DuiLib::CResourceManager::GetText(this_00,(wchar_t *)pCVar3,pwVar2);
  local_8._0_1_ = 2;
  DuiLib::CDuiString::operator=(local_11c,pCVar3);
  local_8 = (uint)local_8._1_3_ << 8;
  DuiLib::CDuiString::~CDuiString(local_98);
  iVar7 = **(int **)(iVar8 + 0x798);
  pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_11c);
  (**(code **)(iVar7 + 0x2c))(pwVar2);
  DuiLib::CDuiString::CDuiString(local_1a0);
  local_8._0_1_ = 3;
  pCVar3 = FUN_00401e90(local_230);
  local_8._0_1_ = 4;
  pCVar3 = (CDuiString *)DuiLib::CDuiString::operator+(pCVar3,(wchar_t *)local_98);
  local_8._0_1_ = 5;
  DuiLib::CDuiString::operator=(local_1a0,pCVar3);
  DuiLib::CDuiString::~CDuiString(local_98);
  local_8._0_1_ = 3;
  DuiLib::CDuiString::~CDuiString(local_230);
  pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_1a0);
  hModule = LoadLibraryW(pwVar2);
  *(HMODULE *)(iVar8 + 0x7a0) = hModule;
  if (hModule == (HMODULE)0x0) {
    DVar4 = GetLastError();
    DuiLib::CDuiString::CDuiString(local_98);
    local_8._0_1_ = 6;
    DuiLib::CDuiString::Format(this_01,(wchar_t *)local_98,L"GetError:%d\n",DVar4);
    DuiLib::CDuiString::~CDuiString(local_98);
    hModule = *(HMODULE *)(iVar8 + 0x7a0);
    if (hModule == (HMODULE)0x0) goto LAB_0041f81c;
  }
  pFVar5 = GetProcAddress(hModule,"installmousehook");
  *(FARPROC *)(iVar8 + 0x764) = pFVar5;
  pFVar5 = GetProcAddress(*(HMODULE *)(iVar8 + 0x7a0),"removemousehook");
  *(FARPROC *)(iVar8 + 0x768) = pFVar5;
  pFVar5 = GetProcAddress(*(HMODULE *)(iVar8 + 0x7a0),"enablemousehook");
  *(FARPROC *)(iVar8 + 0x76c) = pFVar5;
  pFVar5 = GetProcAddress(*(HMODULE *)(iVar8 + 0x7a0),"installhook");
  *(FARPROC *)(iVar8 + 0x770) = pFVar5;
  pFVar5 = GetProcAddress(*(HMODULE *)(iVar8 + 0x7a0),"removehook");
  *(FARPROC *)(iVar8 + 0x774) = pFVar5;
  pFVar5 = GetProcAddress(*(HMODULE *)(iVar8 + 0x7a0),"enablehook");
  *(FARPROC *)(iVar8 + 0x778) = pFVar5;
LAB_0041f81c:
  DuiLib::CDuiString::~CDuiString(local_1a0);
  DuiLib::CDuiString::~CDuiString(local_11c);
  ExceptionList = local_10;
  return;
}


