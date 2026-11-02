// Program: SM809 mouse Software.exe
// Function: FUN_00402ef0
// Entry: 00402ef0
// Body: 00402ef0 - 00403138
// Signature: undefined FUN_00402ef0(void)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void FUN_00402ef0(void)

{
  uint uVar1;
  CDuiString *pCVar2;
  wchar_t *pwVar3;
  HANDLE hFindFile;
  basic_streambuf<char,std::char_traits<char>_> *pbVar4;
  undefined4 *puVar5;
  _WIN32_FIND_DATAW *lpFindFileData;
  LPSECURITY_ATTRIBUTES lpSecurityAttributes;
  CDuiString local_4a0 [132];
  _WIN32_FIND_DATAW local_41c;
  CDuiString local_1cc [132];
  CDuiString local_148 [128];
  CDuiString aCStack_c8 [4];
  int local_c4;
  undefined **local_c0;
  basic_ostream<char,std::char_traits<char>_> local_bc [8];
  int *local_b4;
  int *local_a4;
  int *local_94;
  undefined1 local_84 [12];
  char local_78;
  int local_74;
  int local_70;
  int local_6c;
  basic_ios<char,std::char_traits<char>_> local_5c [72];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_004210c0;
  local_10 = ExceptionList;
  uVar1 = DAT_00432008 ^ (uint)(local_5c + 0x58);
  ExceptionList = &local_10;
  local_14 = uVar1;
  DuiLib::CDuiString::CDuiString(local_148);
  local_8 = 0;
  DuiLib::CDuiString::CDuiString(local_1cc);
  local_8._0_1_ = 1;
  pCVar2 = FUN_00401fb0(local_4a0);
  local_8._0_1_ = 2;
  DuiLib::CDuiString::operator=(local_148,pCVar2);
  local_8 = CONCAT31(local_8._1_3_,1);
  DuiLib::CDuiString::~CDuiString(local_4a0);
  DuiLib::CDuiString::operator+=(local_148,L"Data");
  lpFindFileData = &local_41c;
  pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_148);
  hFindFile = FindFirstFileW(pwVar3,lpFindFileData);
  FindClose(hFindFile);
  if ((hFindFile == (HANDLE)0xffffffff) || (((byte)local_41c.dwFileAttributes & 0x10) == 0)) {
    lpSecurityAttributes = (LPSECURITY_ATTRIBUTES)0x0;
    pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_148);
    CreateDirectoryW(pwVar3,lpSecurityAttributes);
  }
  pCVar2 = (CDuiString *)DuiLib::CDuiString::operator+(local_148,(wchar_t *)local_4a0);
  local_8._0_1_ = 3;
  DuiLib::CDuiString::operator=(local_1cc,pCVar2);
  local_8._0_1_ = 1;
  DuiLib::CDuiString::~CDuiString(local_4a0);
  memset(&local_c4,0,0xb0);
  pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_1cc);
  FUN_00404ee0(&local_c4,pwVar3);
  local_8._0_1_ = 4;
  puVar5 = DAT_0046c380;
  if (DAT_0046c380 != DAT_0046c384) {
    do {
      std::basic_ostream<char,std::char_traits<char>_>::write
                ((basic_ostream<char,std::char_traits<char>_> *)&local_c4,(char *)*puVar5,
                 (ulonglong)uVar1 << 0x20);
      puVar5 = puVar5 + 1;
    } while (puVar5 != DAT_0046c384);
    pbVar4 = FUN_004051d0((basic_streambuf<char,std::char_traits<char>_> *)&local_c0);
    if (pbVar4 == (basic_streambuf<char,std::char_traits<char>_> *)0x0) {
      std::basic_ios<char,std::char_traits<char>_>::setstate
                ((basic_ios<char,std::char_traits<char>_> *)
                 (local_148 + *(int *)(local_c4 + 4) + 0x84),2,false);
    }
  }
  *(undefined ***)(local_148 + *(int *)(local_c4 + 4) + 0x84) =
       std::basic_ofstream<char,std::char_traits<char>_>::vftable;
  *(int *)(local_148 + *(int *)(local_c4 + 4) + 0x80) = *(int *)(local_c4 + 4) + -0x68;
  local_8 = CONCAT31(local_8._1_3_,6);
  local_c0 = std::basic_filebuf<char,std::char_traits<char>_>::vftable;
  if ((local_74 != 0) && ((undefined1 *)*local_b4 == local_84)) {
    *local_b4 = local_70;
    *local_a4 = local_70;
    *local_94 = local_6c - local_70;
  }
  if (local_78 != '\0') {
    FUN_004051d0((basic_streambuf<char,std::char_traits<char>_> *)&local_c0);
  }
  std::basic_streambuf<char,std::char_traits<char>_>::~basic_streambuf<char,std::char_traits<char>_>
            ((basic_streambuf<char,std::char_traits<char>_> *)&local_c0);
  std::basic_ostream<char,std::char_traits<char>_>::~basic_ostream<char,std::char_traits<char>_>
            (local_bc);
  std::basic_ios<char,std::char_traits<char>_>::~basic_ios<char,std::char_traits<char>_>(local_5c);
  DuiLib::CDuiString::~CDuiString(local_1cc);
  DuiLib::CDuiString::~CDuiString(local_148);
  ExceptionList = local_10;
  return;
}


