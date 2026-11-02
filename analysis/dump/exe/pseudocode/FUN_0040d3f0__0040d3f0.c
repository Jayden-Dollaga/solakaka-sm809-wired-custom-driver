// Program: SM809 mouse Software.exe
// Function: FUN_0040d3f0
// Entry: 0040d3f0
// Body: 0040d3f0 - 0040d85f
// Signature: undefined FUN_0040d3f0(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_0040d3f0(int param_1)

{
  uint uVar1;
  CDuiString *pCVar2;
  BOOL BVar3;
  wchar_t *pwVar4;
  int iVar5;
  basic_streambuf<char,std::char_traits<char>_> *pbVar6;
  void *pvVar7;
  CListLabelElementUI *this;
  CDuiString *this_00;
  code *pcVar8;
  CDuiString in_stack_fffff140;
  CDuiString aCStack_ebd [93];
  CDuiString *local_e28;
  tagOFNW local_e24;
  CDuiString local_dcc [132];
  CDuiString local_d48 [132];
  int local_cc4 [4];
  basic_streambuf<char,std::char_traits<char>_> local_cb4 [168];
  CDuiString local_c0c [132];
  CDuiString local_b88 [132];
  wchar_t local_b04 [260];
  wchar_t local_8fc [260];
  wchar_t local_6f4 [260];
  wchar_t local_4ec [260];
  WCHAR local_2e4 [260];
  WCHAR local_dc [50];
  wchar_t local_78 [50];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00422312;
  local_10 = ExceptionList;
  uVar1 = DAT_00432008 ^ (uint)(local_78 + 0x3a);
  ExceptionList = &local_10;
  local_14 = uVar1;
  DuiLib::CDuiString::CDuiString(local_dcc);
  local_8 = 0;
  DuiLib::CDuiString::CDuiString(local_d48);
  local_8._0_1_ = 1;
  pCVar2 = FUN_00401fb0(local_b88);
  local_8._0_1_ = 2;
  DuiLib::CDuiString::operator=(local_d48,pCVar2);
  pcVar8 = ~CDuiString_exref;
  local_8._0_1_ = 1;
  DuiLib::CDuiString::~CDuiString(local_b88);
  DuiLib::CDuiString::GetData(local_d48);
  DuiLib::CDuiString::Format(this_00,(wchar_t *)local_dcc);
  memset(&local_e24,0,0x58);
  memset(local_2e4,0,0x208);
  local_e24.hwndOwner = *(HWND *)(param_1 + 0x14);
  local_e24.lpstrFile = local_2e4;
  local_e24.lStructSize = 0x58;
  local_e24.lpstrFilter = L"Gun Data";
  local_e24.nFilterIndex = 1;
  local_e24.nMaxFile = 0x208;
  local_e24.lpstrInitialDir = DuiLib::CDuiString::operator_wchar_t_const_(local_dcc);
  local_e24.Flags = 0x1804;
  BVar3 = GetOpenFileNameW(&local_e24);
  if (BVar3 != 0) {
    memset(local_cc4,0,0xb8);
    FUN_00404320(local_cc4,local_2e4);
    local_8._0_1_ = 3;
    _wsplitpath_s(local_2e4,local_b04,0x104,local_8fc,0x104,local_4ec,0x104,local_6f4,0x104);
    DuiLib::CDuiString::CDuiString(local_c0c,local_4ec,-1);
    local_8._0_1_ = 4;
    DuiLib::CDuiString::CDuiString(aCStack_ebd + -3,local_c0c);
    local_e28 = (CDuiString *)FUN_00403140(&DAT_0046c398,in_stack_fffff140);
    if (local_e28 != (CDuiString *)0x0) {
      DuiLib::CDuiString::CDuiString(local_b88);
      local_8 = CONCAT31(local_8._1_3_,5);
      pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_c0c);
      wcscpy_s(local_78,0x32,pwVar4);
      pCVar2 = local_e28;
      while (pCVar2 == (CDuiString *)0x1) {
        wsprintfW(local_dc,L"%s_%d");
        DuiLib::CDuiString::operator=(local_b88,local_dc);
        DuiLib::CDuiString::CDuiString(aCStack_ebd + -3,local_b88);
        pCVar2 = (CDuiString *)FUN_00403140(&DAT_0046c398,in_stack_fffff140);
      }
      DuiLib::CDuiString::operator=(local_c0c,local_b88);
      local_8._0_1_ = 4;
      DuiLib::CDuiString::~CDuiString(local_b88);
    }
    iVar5 = std::basic_istream<char,std::char_traits<char>_>::peek
                      ((basic_istream<char,std::char_traits<char>_> *)local_cc4);
    while (iVar5 != -1) {
      pCVar2 = operator_new(0x240);
      local_e28 = pCVar2;
      std::basic_istream<char,std::char_traits<char>_>::read
                ((basic_istream<char,std::char_traits<char>_> *)local_cc4,(char *)pCVar2,
                 (ulonglong)uVar1 << 0x20);
      pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_c0c);
      wcscpy_s((wchar_t *)pCVar2,0x32,pwVar4);
      if (DAT_0046c39c == DAT_0046c3a0) {
        FUN_00405510(DAT_0046c39c,&local_e28);
      }
      else {
        *DAT_0046c39c = pCVar2;
        DAT_0046c39c = DAT_0046c39c + 1;
      }
      iVar5 = std::basic_istream<char,std::char_traits<char>_>::peek
                        ((basic_istream<char,std::char_traits<char>_> *)local_cc4);
    }
    pbVar6 = FUN_004051d0(local_cb4);
    if (pbVar6 == (basic_streambuf<char,std::char_traits<char>_> *)0x0) {
      std::basic_ios<char,std::char_traits<char>_>::setstate
                ((basic_ios<char,std::char_traits<char>_> *)
                 ((int)local_cc4 + *(int *)(local_cc4[0] + 4)),2,false);
    }
    local_e28 = operator_new(0x84);
    local_8._0_1_ = 6;
    pvVar7 = (void *)DuiLib::CDuiString::CDuiString(local_e28,local_c0c);
    local_8._0_1_ = 4;
    DuiLib::CStdPtrArray::Add((CStdPtrArray *)(param_1 + 0x19c),pvVar7);
    DuiLib::CDuiString::CDuiString(local_b88,local_c0c);
    local_8._0_1_ = 7;
    this = operator_new(0x570);
    local_8._0_1_ = 8;
    local_e28 = (CDuiString *)this;
    DuiLib::CListLabelElementUI::CListLabelElementUI(this);
    *(undefined ***)this = DuiLib::CListLabelElementUI::vftable;
    local_8._0_1_ = 7;
    pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_b88);
    DuiLib::CControlUI::SetText((CControlUI *)this,pwVar4);
    (**(code **)(*(int *)this + 0x88))();
    (**(code **)(*(int *)(*(int *)(param_1 + 0x1b0) + 0x558) + 0x10))();
    pcVar8 = ~CDuiString_exref;
    local_8._0_1_ = 4;
    DuiLib::CDuiString::~CDuiString(local_b88);
    DuiLib::CStdPtrArray::GetSize((CStdPtrArray *)(param_1 + 0x19c));
    (**(code **)(*(int *)(*(int *)(param_1 + 0x1b0) + 0x6a0) + 0xc))();
    FUN_00403350();
    DuiLib::CDuiString::~CDuiString(local_c0c);
    FUN_00402e30(local_cc4);
  }
  (*pcVar8)();
  (*pcVar8)();
  ExceptionList = local_10;
  return;
}


