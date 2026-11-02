// Program: SM809 mouse Software.exe
// Function: FUN_00416c70
// Entry: 00416c70
// Body: 00416c70 - 00417537
// Signature: undefined FUN_00416c70(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN_00416c70(int param_1)

{
  uint uVar1;
  CDuiString *pCVar2;
  wchar_t *pwVar3;
  basic_streambuf<char,std::char_traits<char>_> *pbVar4;
  int iVar5;
  CListLabelElementUI *pCVar6;
  int *piVar7;
  code *pcVar8;
  undefined4 *puVar9;
  void *pvVar10;
  int *piVar11;
  CDuiString local_40c [136];
  CListLabelElementUI *local_384;
  CDuiString *local_380;
  int local_37c;
  CListLabelElementUI *local_378;
  int local_374 [3];
  byte abStack_368 [4];
  basic_streambuf<char,std::char_traits<char>_> local_364 [168];
  CDuiString local_2bc [136];
  CDuiString local_234 [136];
  CDuiString local_1ac [136];
  CDuiString local_124 [136];
  CDuiString local_9c [136];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  pcVar8 = CDuiString_exref;
  local_8 = 0xffffffff;
  puStack_c = &LAB_004233fb;
  local_10 = ExceptionList;
  uVar1 = DAT_00432008 ^ (uint)(local_9c + 0x98);
  ExceptionList = &local_10;
  local_37c = param_1;
  local_14 = uVar1;
  DuiLib::CDuiString::CDuiString(local_9c);
  local_8 = 0;
  DuiLib::CDuiString::CDuiString(local_1ac);
  local_8._0_1_ = 1;
  DuiLib::CDuiString::CDuiString(local_2bc);
  local_8._0_1_ = 2;
  DuiLib::CDuiString::CDuiString(local_124);
  local_8._0_1_ = 3;
  pCVar2 = FUN_00401fb0(local_40c);
  local_8._0_1_ = 4;
  DuiLib::CDuiString::operator=(local_9c,pCVar2);
  local_8._0_1_ = 3;
  DuiLib::CDuiString::~CDuiString(local_40c);
  pCVar2 = (CDuiString *)DuiLib::CDuiString::operator+(local_9c,(wchar_t *)local_40c);
  local_8._0_1_ = 5;
  DuiLib::CDuiString::operator=(local_124,pCVar2);
  local_8._0_1_ = 3;
  DuiLib::CDuiString::~CDuiString(local_40c);
  memset(local_374,0,0xb8);
  pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_124);
  FUN_00404320(local_374,pwVar3);
  local_8 = CONCAT31(local_8._1_3_,6);
  if ((abStack_368[*(int *)(local_374[0] + 4)] & 6) == 0) {
    std::basic_istream<char,std::char_traits<char>_>::read
              ((basic_istream<char,std::char_traits<char>_> *)local_374,(char *)&DAT_00432aa8,
               (ulonglong)uVar1 << 0x20);
  }
  else {
    DAT_00432aa8 = 0;
    _DAT_00432aac = 0;
    FUN_00402b20();
  }
  pbVar4 = FUN_004051d0(local_364);
  if (pbVar4 == (basic_streambuf<char,std::char_traits<char>_> *)0x0) {
    std::basic_ios<char,std::char_traits<char>_>::setstate
              ((basic_ios<char,std::char_traits<char>_> *)
               ((int)local_374 + *(int *)(local_374[0] + 4)),2,false);
  }
  FUN_00402e30(local_374);
  DuiLib::CDuiString::~CDuiString(local_124);
  DuiLib::CDuiString::~CDuiString(local_2bc);
  DuiLib::CDuiString::~CDuiString(local_1ac);
  local_8 = 0xffffffff;
  DuiLib::CDuiString::~CDuiString(local_9c);
  FUN_004037f0();
  DuiLib::CDuiString::CDuiString(local_124);
  local_8 = 7;
  DuiLib::CDuiString::CDuiString(local_2bc);
  local_8._0_1_ = 8;
  DuiLib::CDuiString::CDuiString(local_9c);
  local_8._0_1_ = 9;
  pCVar2 = FUN_00401fb0(local_1ac);
  local_8._0_1_ = 10;
  DuiLib::CDuiString::operator=(local_124,pCVar2);
  local_8._0_1_ = 9;
  DuiLib::CDuiString::~CDuiString(local_1ac);
  pCVar2 = (CDuiString *)DuiLib::CDuiString::operator+(local_124,(wchar_t *)local_1ac);
  local_8._0_1_ = 0xb;
  DuiLib::CDuiString::operator=(local_9c,pCVar2);
  local_8._0_1_ = 9;
  DuiLib::CDuiString::~CDuiString(local_1ac);
  memset(local_374,0,0xb8);
  pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_9c);
  FUN_00404320(local_374,pwVar3);
  local_8 = CONCAT31(local_8._1_3_,0xc);
  if (((abStack_368[*(int *)(local_374[0] + 4)] & 6) == 0) &&
     (iVar5 = std::basic_istream<char,std::char_traits<char>_>::peek
                        ((basic_istream<char,std::char_traits<char>_> *)local_374), iVar5 != -1)) {
    do {
      pCVar6 = operator_new(0x358);
      local_378 = pCVar6;
      std::basic_istream<char,std::char_traits<char>_>::read
                ((basic_istream<char,std::char_traits<char>_> *)local_374,(char *)pCVar6,
                 (ulonglong)uVar1 << 0x20);
      if (DAT_0046c384 == DAT_0046c388) {
        FUN_00405690(DAT_0046c384,&local_378);
      }
      else {
        *DAT_0046c384 = (int)pCVar6;
        DAT_0046c384 = DAT_0046c384 + 1;
      }
      iVar5 = std::basic_istream<char,std::char_traits<char>_>::peek
                        ((basic_istream<char,std::char_traits<char>_> *)local_374);
    } while (iVar5 != -1);
    pcVar8 = CDuiString_exref;
  }
  pbVar4 = FUN_004051d0(local_364);
  if (pbVar4 == (basic_streambuf<char,std::char_traits<char>_> *)0x0) {
    std::basic_ios<char,std::char_traits<char>_>::setstate
              ((basic_ios<char,std::char_traits<char>_> *)
               ((int)local_374 + *(int *)(local_374[0] + 4)),2,false);
  }
  FUN_00402e30(local_374);
  DuiLib::CDuiString::~CDuiString(local_9c);
  DuiLib::CDuiString::~CDuiString(local_2bc);
  local_8 = 0xffffffff;
  DuiLib::CDuiString::~CDuiString(local_124);
  (*pcVar8)();
  local_8 = 0xd;
  (*pcVar8)();
  local_8._0_1_ = 0xe;
  (*pcVar8)();
  local_8._0_1_ = 0xf;
  pCVar2 = FUN_00401fb0(local_1ac);
  local_8._0_1_ = 0x10;
  DuiLib::CDuiString::operator=(local_124,pCVar2);
  local_8._0_1_ = 0xf;
  DuiLib::CDuiString::~CDuiString(local_1ac);
  pCVar2 = (CDuiString *)DuiLib::CDuiString::operator+(local_124,(wchar_t *)local_1ac);
  local_8._0_1_ = 0x11;
  DuiLib::CDuiString::operator=(local_9c,pCVar2);
  local_8._0_1_ = 0xf;
  DuiLib::CDuiString::~CDuiString(local_1ac);
  memset(local_374,0,0xb8);
  pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_9c);
  FUN_00404320(local_374,pwVar3);
  local_8 = CONCAT31(local_8._1_3_,0x12);
  if ((abStack_368[*(int *)(local_374[0] + 4)] & 6) == 0) {
    iVar5 = std::basic_istream<char,std::char_traits<char>_>::peek
                      ((basic_istream<char,std::char_traits<char>_> *)local_374);
    while (iVar5 != -1) {
      pCVar6 = operator_new(0x240);
      local_378 = pCVar6;
      std::basic_istream<char,std::char_traits<char>_>::read
                ((basic_istream<char,std::char_traits<char>_> *)local_374,(char *)pCVar6,
                 (ulonglong)uVar1 << 0x20);
      if (DAT_0046c39c == DAT_0046c3a0) {
        FUN_00405510(DAT_0046c39c,&local_378);
      }
      else {
        *DAT_0046c39c = (int)pCVar6;
        DAT_0046c39c = DAT_0046c39c + 1;
      }
      iVar5 = std::basic_istream<char,std::char_traits<char>_>::peek
                        ((basic_istream<char,std::char_traits<char>_> *)local_374);
    }
  }
  pbVar4 = FUN_004051d0(local_364);
  if (pbVar4 == (basic_streambuf<char,std::char_traits<char>_> *)0x0) {
    std::basic_ios<char,std::char_traits<char>_>::setstate
              ((basic_ios<char,std::char_traits<char>_> *)
               ((int)local_374 + *(int *)(local_374[0] + 4)),2,false);
  }
  FUN_00402e30(local_374);
  DuiLib::CDuiString::~CDuiString(local_9c);
  DuiLib::CDuiString::~CDuiString(local_2bc);
  local_8 = 0xffffffff;
  DuiLib::CDuiString::~CDuiString(local_124);
  puVar9 = DAT_0046c38c;
  if (DAT_0046c38c != DAT_0046c390) {
    do {
      DuiLib::CDuiString::CDuiString(local_9c,(wchar_t *)*puVar9,-1);
      local_8 = 0x13;
      pCVar6 = operator_new(0x570);
      local_8._0_1_ = 0x14;
      local_378 = pCVar6;
      DuiLib::CListLabelElementUI::CListLabelElementUI(pCVar6);
      *(undefined ***)pCVar6 = DuiLib::CListLabelElementUI::vftable;
      local_8 = CONCAT31(local_8._1_3_,0x13);
      pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_9c);
      DuiLib::CControlUI::SetText((CControlUI *)pCVar6,pwVar3);
      (**(code **)(*(int *)pCVar6 + 0x88))(0x19);
      (**(code **)(*(int *)(*(int *)(local_37c + 0x16fc) + 0x558) + 0x10))(pCVar6);
      local_8 = 0xffffffff;
      DuiLib::CDuiString::~CDuiString(local_9c);
      puVar9 = puVar9 + 1;
    } while (puVar9 != DAT_0046c390);
    param_1 = local_37c;
  }
  (**(code **)(*(int *)(*(int *)(param_1 + 0x16fc) + 0x6a0) + 0xc))(DAT_00432aa8,0);
  if (DAT_0046c38c == DAT_0046c390) {
    pvVar10 = (void *)0x0;
  }
  else {
    if ((uint)((int)DAT_0046c390 - (int)DAT_0046c38c >> 2) <= DAT_00432aa8) {
                    /* WARNING: Subroutine does not return */
      FUN_004050f0();
    }
    pvVar10 = (void *)DAT_0046c38c[DAT_00432aa8];
  }
  DAT_00432aa0 = pvVar10;
  memcpy(&DAT_0044f730,pvVar10,0x1cc50);
  (**(code **)(**(int **)(param_1 + 0x170c) + 0x2c))(pvVar10);
  DuiLib::CDuiString::CDuiString(local_9c);
  local_378 = (CListLabelElementUI *)(param_1 + 0xe44);
  local_8 = 0x15;
  DuiLib::CStdPtrArray::Empty((CStdPtrArray *)local_378);
  piVar7 = DAT_0046c384;
  piVar11 = DAT_0046c380;
  if (DAT_0046c380 != DAT_0046c384) {
    do {
      pwVar3 = (wchar_t *)*piVar11;
      if (*(int *)(pwVar3 + 0x6a) == 1) {
        DuiLib::CDuiString::operator=(local_9c,pwVar3);
        local_380 = operator_new(0x84);
        local_8._0_1_ = 0x16;
        pvVar10 = (void *)DuiLib::CDuiString::CDuiString(local_380,local_9c);
        local_8._0_1_ = 0x15;
        DuiLib::CStdPtrArray::Add((CStdPtrArray *)local_378,pvVar10);
        DuiLib::CDuiString::CDuiString(local_234,pwVar3,-1);
        local_8._0_1_ = 0x17;
        pCVar6 = operator_new(0x570);
        local_8._0_1_ = 0x18;
        local_384 = pCVar6;
        DuiLib::CListLabelElementUI::CListLabelElementUI(pCVar6);
        *(undefined ***)pCVar6 = DuiLib::CListLabelElementUI::vftable;
        local_8._0_1_ = 0x17;
        pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_234);
        DuiLib::CControlUI::SetText((CControlUI *)pCVar6,pwVar3);
        (**(code **)(*(int *)pCVar6 + 0x88))(0x19);
        (**(code **)(*(int *)(*(int *)(local_37c + 0xe78) + 0x558) + 0x10))(pCVar6);
        local_8 = CONCAT31(local_8._1_3_,0x15);
        DuiLib::CDuiString::~CDuiString(local_234);
        piVar7 = DAT_0046c384;
      }
      piVar11 = piVar11 + 1;
    } while (piVar11 != piVar7);
    param_1 = local_37c;
  }
  iVar5 = DuiLib::CStdPtrArray::GetSize((CStdPtrArray *)(param_1 + 0xe44));
  if (0 < iVar5) {
    (**(code **)(*(int *)(*(int *)(param_1 + 0xe78) + 0x6a0) + 0xc))(0,0);
  }
  local_8 = 0xffffffff;
  DuiLib::CDuiString::~CDuiString(local_9c);
  DuiLib::CDuiString::CDuiString(local_234);
  local_378 = (CListLabelElementUI *)(param_1 + 0x1094);
  local_8 = 0x19;
  DuiLib::CStdPtrArray::Empty((CStdPtrArray *)local_378);
  piVar7 = DAT_0046c39c;
  piVar11 = DAT_0046c398;
  if (DAT_0046c398 != DAT_0046c39c) {
    do {
      pwVar3 = (wchar_t *)*piVar11;
      if (*(int *)(pwVar3 + 0x68) == 1) {
        DuiLib::CDuiString::operator=(local_234,pwVar3);
        local_384 = operator_new(0x84);
        local_8._0_1_ = 0x1a;
        pvVar10 = (void *)DuiLib::CDuiString::CDuiString((CDuiString *)local_384,local_234);
        local_8._0_1_ = 0x19;
        DuiLib::CStdPtrArray::Add((CStdPtrArray *)local_378,pvVar10);
        DuiLib::CDuiString::CDuiString(local_40c,pwVar3,-1);
        local_8._0_1_ = 0x1b;
        pCVar6 = operator_new(0x570);
        local_8._0_1_ = 0x1c;
        local_380 = (CDuiString *)pCVar6;
        DuiLib::CListLabelElementUI::CListLabelElementUI(pCVar6);
        *(undefined ***)pCVar6 = DuiLib::CListLabelElementUI::vftable;
        local_8._0_1_ = 0x1b;
        pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_40c);
        DuiLib::CControlUI::SetText((CControlUI *)pCVar6,pwVar3);
        (**(code **)(*(int *)pCVar6 + 0x88))(0x19);
        (**(code **)(*(int *)(*(int *)(local_37c + 0x10a8) + 0x558) + 0x10))(pCVar6);
        local_8 = CONCAT31(local_8._1_3_,0x19);
        DuiLib::CDuiString::~CDuiString(local_40c);
        piVar7 = DAT_0046c39c;
      }
      piVar11 = piVar11 + 1;
    } while (piVar11 != piVar7);
    param_1 = local_37c;
  }
  iVar5 = DuiLib::CStdPtrArray::GetSize((CStdPtrArray *)(param_1 + 0x1094));
  if (0 < iVar5) {
    (**(code **)(*(int *)(*(int *)(param_1 + 0x10a8) + 0x6a0) + 0xc))(0,0);
  }
  local_8 = 0xffffffff;
  DuiLib::CDuiString::~CDuiString(local_234);
  FUN_00417540(param_1);
  ExceptionList = local_10;
  return;
}


