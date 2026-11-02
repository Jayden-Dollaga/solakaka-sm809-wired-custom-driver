// Program: SM809 mouse Software.exe
// Function: FUN_004183f0
// Entry: 004183f0
// Body: 004183f0 - 004187b4
// Signature: undefined FUN_004183f0(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_004183f0(int param_1)

{
  uint uVar1;
  CDuiString *pCVar2;
  BOOL BVar3;
  CListLabelElementUI *pCVar4;
  basic_streambuf<char,std::char_traits<char>_> *pbVar5;
  wchar_t *pwVar6;
  int iVar7;
  CDuiString *this;
  CDuiString in_stack_fffff95c;
  CDuiString aCStack_6a1 [93];
  CListLabelElementUI *local_60c;
  int local_608;
  tagOFNW local_604;
  CDuiString local_5ac [132];
  CDuiString local_528 [132];
  int local_4a4 [4];
  basic_streambuf<char,std::char_traits<char>_> local_494 [168];
  CDuiString local_3ec [132];
  CDuiString local_368 [132];
  WCHAR local_2e4 [260];
  WCHAR local_dc [50];
  wchar_t local_78 [50];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_0042364d;
  local_10 = ExceptionList;
  uVar1 = DAT_00432008 ^ (uint)(local_78 + 0x3a);
  ExceptionList = &local_10;
  local_14 = uVar1;
  DuiLib::CDuiString::CDuiString(local_5ac);
  local_8 = 0;
  DuiLib::CDuiString::CDuiString(local_528);
  local_8._0_1_ = 1;
  pCVar2 = FUN_00401fb0(local_368);
  local_8._0_1_ = 2;
  DuiLib::CDuiString::operator=(local_528,pCVar2);
  local_8._0_1_ = 1;
  DuiLib::CDuiString::~CDuiString(local_368);
  DuiLib::CDuiString::GetData(local_528);
  DuiLib::CDuiString::Format(this,(wchar_t *)local_5ac);
  memset(&local_604,0,0x58);
  memset(local_2e4,0,0x208);
  local_604.hwndOwner = *(HWND *)(param_1 + 4);
  local_604.lpstrFile = local_2e4;
  local_604.lStructSize = 0x58;
  local_604.lpstrFilter = L"Profile Data";
  local_604.nFilterIndex = 1;
  local_604.nMaxFile = 0x208;
  local_604.lpstrInitialDir = DuiLib::CDuiString::operator_wchar_t_const_(local_5ac);
  local_604.Flags = 0x1804;
  BVar3 = GetOpenFileNameW(&local_604);
  if (BVar3 != 0) {
    memset(local_4a4,0,0xb8);
    FUN_00404320(local_4a4,local_2e4);
    local_8 = CONCAT31(local_8._1_3_,3);
    pCVar4 = operator_new(0x1cc50);
    local_60c = pCVar4;
    std::basic_istream<char,std::char_traits<char>_>::read
              ((basic_istream<char,std::char_traits<char>_> *)local_4a4,(char *)pCVar4,
               (ulonglong)uVar1 << 0x20);
    pbVar5 = FUN_004051d0(local_494);
    if (pbVar5 == (basic_streambuf<char,std::char_traits<char>_> *)0x0) {
      std::basic_ios<char,std::char_traits<char>_>::setstate
                ((basic_ios<char,std::char_traits<char>_> *)
                 ((int)local_4a4 + *(int *)(local_4a4[0] + 4)),2,false);
    }
    DuiLib::CDuiString::CDuiString(local_3ec);
    local_8._0_1_ = 4;
    DuiLib::CDuiString::operator=(local_3ec,(wchar_t *)pCVar4);
    DuiLib::CDuiString::CDuiString(aCStack_6a1 + -3,local_3ec);
    local_608 = FUN_004039e0(in_stack_fffff95c);
    if (local_608 != 0) {
      DuiLib::CDuiString::CDuiString(local_368);
      local_8 = CONCAT31(local_8._1_3_,5);
      pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_3ec);
      wcscpy_s(local_78,0x32,pwVar6);
      iVar7 = local_608;
      while (iVar7 == 1) {
        wsprintfW(local_dc,L"%s_%d");
        DuiLib::CDuiString::operator=(local_368,local_dc);
        DuiLib::CDuiString::CDuiString(aCStack_6a1 + -3,local_368);
        iVar7 = FUN_004039e0(in_stack_fffff95c);
      }
      DuiLib::CDuiString::operator=(local_3ec,local_368);
      local_8._0_1_ = 4;
      DuiLib::CDuiString::~CDuiString(local_368);
    }
    pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_3ec);
    wcscpy_s((wchar_t *)pCVar4,0x32,pwVar6);
    if (DAT_0046c390 == DAT_0046c394) {
      FUN_00405390(DAT_0046c390,&local_60c);
    }
    else {
      *DAT_0046c390 = pCVar4;
      DAT_0046c390 = DAT_0046c390 + 1;
    }
    DuiLib::CDuiString::CDuiString(local_368,(wchar_t *)pCVar4,-1);
    local_8._0_1_ = 6;
    pCVar4 = operator_new(0x570);
    local_8._0_1_ = 7;
    local_60c = pCVar4;
    DuiLib::CListLabelElementUI::CListLabelElementUI(pCVar4);
    *(undefined ***)pCVar4 = DuiLib::CListLabelElementUI::vftable;
    local_8._0_1_ = 6;
    pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_368);
    DuiLib::CControlUI::SetText((CControlUI *)pCVar4,pwVar6);
    (**(code **)(*(int *)pCVar4 + 0x88))();
    (**(code **)(*(int *)(*(int *)(param_1 + 0x16fc) + 0x558) + 0x10))();
    local_8._0_1_ = 4;
    DuiLib::CDuiString::~CDuiString(local_368);
    (**(code **)(*(int *)(*(int *)(param_1 + 0x16fc) + 0x6a0) + 0xc))();
    DuiLib::CDuiString::~CDuiString(local_3ec);
    FUN_00402e30(local_4a4);
  }
  DuiLib::CDuiString::~CDuiString(local_528);
  DuiLib::CDuiString::~CDuiString(local_5ac);
  ExceptionList = local_10;
  return;
}


