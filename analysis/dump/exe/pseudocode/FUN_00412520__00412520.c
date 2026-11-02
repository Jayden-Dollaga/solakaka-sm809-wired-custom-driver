// Program: SM809 mouse Software.exe
// Function: FUN_00412520
// Entry: 00412520
// Body: 00412520 - 00412cb4
// Signature: undefined FUN_00412520(wchar_t * param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_00412520(wchar_t *param_1)

{
  uint uVar1;
  CDuiString *pCVar2;
  BOOL BVar3;
  int iVar4;
  wchar_t *pwVar5;
  basic_streambuf<char,std::char_traits<char>_> *pbVar6;
  wchar_t *pwVar7;
  void *pvVar8;
  CListLabelElementUI *this;
  CDuiString *this_00;
  CDuiString in_stack_fffff030;
  CDuiString aCStack_fcd [121];
  CDuiString CVar9;
  CDuiString in_stack_fffff0b4;
  CDuiString aCStack_f49 [93];
  wchar_t *local_eb8;
  wchar_t *local_eb4;
  CListLabelElementUI *local_eb0;
  wchar_t *local_eac;
  tagOFNW local_ea8;
  CDuiString local_e50 [132];
  CDuiString local_dcc [132];
  int local_d48 [4];
  basic_streambuf<char,std::char_traits<char>_> local_d38 [168];
  CDuiString local_c90 [132];
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
  puStack_c = &LAB_00422002;
  local_10 = ExceptionList;
  uVar1 = DAT_00432008 ^ (uint)(local_78 + 0x3a);
  ExceptionList = &local_10;
  local_eb4 = param_1;
  local_14 = uVar1;
  DuiLib::CDuiString::CDuiString(local_e50);
  local_8 = 0;
  DuiLib::CDuiString::CDuiString(local_dcc);
  local_8._0_1_ = 1;
  pCVar2 = FUN_00401fb0(local_b88);
  local_8._0_1_ = 2;
  DuiLib::CDuiString::operator=(local_dcc,pCVar2);
  local_8._0_1_ = 1;
  DuiLib::CDuiString::~CDuiString(local_b88);
  DuiLib::CDuiString::GetData(local_dcc);
  DuiLib::CDuiString::Format(this_00,(wchar_t *)local_e50);
  memset(&local_ea8,0,0x58);
  memset(local_2e4,0,0x208);
  local_ea8.hwndOwner = *(HWND *)(param_1 + 10);
  local_ea8.lpstrFile = local_2e4;
  local_ea8.lStructSize = 0x58;
  local_ea8.lpstrFilter = L"Macro Data";
  local_ea8.nFilterIndex = 1;
  local_ea8.nMaxFile = 0x208;
  local_ea8.lpstrInitialDir = DuiLib::CDuiString::operator_wchar_t_const_(local_e50);
  local_ea8.Flags = 0x1804;
  BVar3 = GetOpenFileNameW(&local_ea8);
  if (BVar3 != 0) {
    memset(local_d48,0,0xb8);
    FUN_00404320(local_d48,local_2e4);
    local_8._0_1_ = 3;
    _wsplitpath_s(local_2e4,local_b04,0x104,local_8fc,0x104,local_4ec,0x104,local_6f4,0x104);
    DuiLib::CDuiString::CDuiString(local_c0c);
    local_8 = CONCAT31(local_8._1_3_,4);
    if ((*(int *)(param_1 + 0x188) < 0) ||
       (iVar4 = DuiLib::CStdPtrArray::GetSize((CStdPtrArray *)(param_1 + 0x182)),
       iVar4 <= *(int *)(param_1 + 0x188))) {
      pwVar5 = operator_new(0x358);
      local_eb4 = pwVar5;
      std::basic_istream<char,std::char_traits<char>_>::read
                ((basic_istream<char,std::char_traits<char>_> *)local_d48,(char *)pwVar5,
                 (ulonglong)uVar1 << 0x20);
      pbVar6 = FUN_004051d0(local_d38);
      if (pbVar6 == (basic_streambuf<char,std::char_traits<char>_> *)0x0) {
        std::basic_ios<char,std::char_traits<char>_>::setstate
                  ((basic_ios<char,std::char_traits<char>_> *)
                   ((int)local_d48 + *(int *)(local_d48[0] + 4)),2,false);
      }
      DuiLib::CDuiString::operator=(local_c0c,pwVar5);
      DuiLib::CDuiString::CDuiString(aCStack_f49 + -3,local_c0c);
      local_eac = (wchar_t *)FUN_00403140(&DAT_0046c380,in_stack_fffff0b4);
      if (local_eac != (wchar_t *)0x0) {
        DuiLib::CDuiString::CDuiString(local_b88);
        local_8 = CONCAT31(local_8._1_3_,5);
        pwVar5 = DuiLib::CDuiString::operator_wchar_t_const_(local_c0c);
        wcscpy_s(local_dc,0x32,pwVar5);
        pwVar5 = local_eac;
        while (pwVar5 == (wchar_t *)0x1) {
          wsprintfW(local_78,L"%s_%d");
          DuiLib::CDuiString::operator=(local_b88,local_78);
          DuiLib::CDuiString::CDuiString(aCStack_f49 + -3,local_b88);
          pwVar5 = (wchar_t *)FUN_00403140(&DAT_0046c380,in_stack_fffff0b4);
        }
        DuiLib::CDuiString::operator=(local_c0c,local_b88);
        local_8 = CONCAT31(local_8._1_3_,4);
        DuiLib::CDuiString::~CDuiString(local_b88);
      }
      pwVar5 = operator_new(0x358);
      local_eac = pwVar5;
      memset(pwVar5,0,0x358);
      pwVar7 = DuiLib::CDuiString::operator_wchar_t_const_(local_c0c);
      wcscpy_s(pwVar5,0x32,pwVar7);
      pwVar5[0x6a] = L'\x01';
      pwVar5[0x6b] = L'\0';
      if (DAT_0046c384 == DAT_0046c388) {
        FUN_00405690(DAT_0046c384,&local_eac);
      }
      else {
        *DAT_0046c384 = pwVar5;
        DAT_0046c384 = DAT_0046c384 + 1;
      }
      local_eb0 = operator_new(0x84);
      local_8._0_1_ = 6;
      pvVar8 = (void *)DuiLib::CDuiString::CDuiString((CDuiString *)local_eb0,local_c0c);
      local_8 = CONCAT31(local_8._1_3_,4);
      DuiLib::CStdPtrArray::Add((CStdPtrArray *)(param_1 + 0x182),pvVar8);
      pwVar7 = DuiLib::CDuiString::operator_wchar_t_const_(local_c0c);
      pwVar5 = local_eb4;
      wcscpy_s(local_eb4,0x32,pwVar7);
      if (DAT_0046c384 == DAT_0046c388) {
        FUN_00405690(DAT_0046c384,&local_eb4);
      }
      else {
        *DAT_0046c384 = pwVar5;
        DAT_0046c384 = DAT_0046c384 + 1;
      }
      DuiLib::CDuiString::CDuiString(local_b88,local_c0c);
      local_8._0_1_ = 7;
      this = operator_new(0x570);
      local_8._0_1_ = 8;
      local_eb0 = this;
      DuiLib::CListLabelElementUI::CListLabelElementUI(this);
      *(undefined ***)this = DuiLib::CListLabelElementUI::vftable;
      local_8._0_1_ = 7;
      pwVar5 = DuiLib::CDuiString::operator_wchar_t_const_(local_b88);
      DuiLib::CControlUI::SetText((CControlUI *)this,pwVar5);
      (**(code **)(*(int *)this + 0x88))();
      (**(code **)(*(int *)(*(int *)(param_1 + 0x19c) + 0x558) + 0x10))();
      local_8._0_1_ = 4;
      DuiLib::CDuiString::~CDuiString(local_b88);
      DuiLib::CStdPtrArray::GetSize((CStdPtrArray *)(param_1 + 0x182));
      (**(code **)(*(int *)(*(int *)(param_1 + 0x19c) + 0x6a0) + 0xc))();
      FUN_00402ef0();
      (**(code **)(*(int *)(*(int *)(param_1 + 0x1cc) + 0x6c8) + 0xc))();
    }
    else {
      pwVar5 = operator_new(0x358);
      local_eb8 = pwVar5;
      std::basic_istream<char,std::char_traits<char>_>::read
                ((basic_istream<char,std::char_traits<char>_> *)local_d48,(char *)pwVar5,
                 (ulonglong)uVar1 << 0x20);
      pbVar6 = FUN_004051d0(local_d38);
      if (pbVar6 == (basic_streambuf<char,std::char_traits<char>_> *)0x0) {
        std::basic_ios<char,std::char_traits<char>_>::setstate
                  ((basic_ios<char,std::char_traits<char>_> *)
                   ((int)local_d48 + *(int *)(local_d48[0] + 4)),2,false);
      }
      pCVar2 = DuiLib::CStdPtrArray::operator[]
                         ((CStdPtrArray *)(param_1 + 0x182),*(int *)(param_1 + 0x188));
      pwVar7 = DuiLib::CDuiString::GetData(pCVar2);
      DuiLib::CDuiString::operator=(local_c0c,pwVar7);
      pwVar7 = DuiLib::CDuiString::operator_wchar_t_const_(local_c0c);
      wcscpy_s(pwVar5,0x32,pwVar7);
      DuiLib::CDuiString::CDuiString(local_c90);
      local_8._0_1_ = 9;
      DuiLib::CDuiString::operator=(local_c90,local_4ec);
      pCVar2 = local_c90;
      local_eac = (wchar_t *)(aCStack_f49 + -3);
      DuiLib::CDuiString::CDuiString(aCStack_f49 + -3,pCVar2);
      local_8._0_1_ = 10;
      DuiLib::CDuiString::CDuiString(aCStack_fcd + -3,local_c0c);
      local_8._0_1_ = 9;
      local_eac = (wchar_t *)FUN_00403220(&DAT_0046c380,in_stack_fffff030);
      CVar9 = SUB41(pCVar2,0);
      if (local_eac != (wchar_t *)0x0) {
        DuiLib::CDuiString::CDuiString(local_b88);
        local_8 = CONCAT31(local_8._1_3_,0xb);
        pwVar5 = DuiLib::CDuiString::operator_wchar_t_const_(local_c90);
        wcscpy_s(local_78,0x32,pwVar5);
        pwVar5 = local_eac;
        while (CVar9 = SUB41(pCVar2,0), pwVar5 == (wchar_t *)0x1) {
          wsprintfW(local_dc,L"%s_%d");
          DuiLib::CDuiString::operator=(local_b88,local_dc);
          local_eb0 = (CListLabelElementUI *)(aCStack_f49 + -3);
          pCVar2 = local_b88;
          DuiLib::CDuiString::CDuiString(aCStack_f49 + -3,pCVar2);
          local_8._0_1_ = 0xc;
          DuiLib::CDuiString::CDuiString(aCStack_fcd + -3,local_c0c);
          local_8 = CONCAT31(local_8._1_3_,0xb);
          pwVar5 = (wchar_t *)FUN_00403220(&DAT_0046c380,in_stack_fffff030);
        }
        DuiLib::CDuiString::operator=(local_c90,local_b88);
        local_8._0_1_ = 9;
        DuiLib::CDuiString::~CDuiString(local_b88);
        pwVar5 = local_eb8;
      }
      pwVar7 = DuiLib::CDuiString::operator_wchar_t_const_(local_c90);
      wcscpy_s(pwVar5 + 0x32,0x32,pwVar7);
      if (DAT_0046c384 == DAT_0046c388) {
        FUN_00405690(DAT_0046c384,&local_eb8);
      }
      else {
        *DAT_0046c384 = pwVar5;
        DAT_0046c384 = DAT_0046c384 + 1;
      }
      FUN_00402ef0();
      DuiLib::CStdPtrArray::Add
                ((CStdPtrArray *)(local_eb4 + 0x17c),
                 (void *)(((int)DAT_0046c384 - DAT_0046c380 >> 2) + -1));
      DuiLib::CDuiString::CDuiString(aCStack_fcd + 0x7d,local_c90);
      pwVar5 = local_eb4;
      FUN_00413500((int)local_eb4,CVar9);
      iVar4 = *(int *)(*(int *)(pwVar5 + 0x1cc) + 0x6c8);
      (**(code **)(*(int *)(*(int *)(pwVar5 + 0x1cc) + 0x558) + 0xc))();
      (**(code **)(iVar4 + 0xc))();
      DuiLib::CDuiString::~CDuiString(local_c90);
    }
    DuiLib::CDuiString::~CDuiString(local_c0c);
    FUN_00402e30(local_d48);
  }
  DuiLib::CDuiString::~CDuiString(local_dcc);
  DuiLib::CDuiString::~CDuiString(local_e50);
  ExceptionList = local_10;
  return;
}


