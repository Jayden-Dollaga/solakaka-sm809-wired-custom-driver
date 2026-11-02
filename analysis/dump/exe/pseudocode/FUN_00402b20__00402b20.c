// Program: SM809 mouse Software.exe
// Function: FUN_00402b20
// Entry: 00402b20
// Body: 00402b20 - 00402d6d
// Signature: undefined4 FUN_00402b20(void)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

undefined4 FUN_00402b20(void)

{
  uint uVar1;
  CDuiString *pCVar2;
  wchar_t *pwVar3;
  HANDLE hFindFile;
  basic_ostream<char,struct_std::char_traits<char>_> *pbVar4;
  basic_streambuf<char,std::char_traits<char>_> *pbVar5;
  _WIN32_FIND_DATAW *lpFindFileData;
  LPSECURITY_ATTRIBUTES lpSecurityAttributes;
  CDuiString local_4b4 [140];
  char *local_428;
  _WIN32_FIND_DATAW local_424;
  CDuiString local_1d4 [136];
  CDuiString local_14c [132];
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
  puStack_c = &LAB_00421030;
  local_10 = ExceptionList;
  uVar1 = DAT_00432008 ^ (uint)(local_5c + 0x58);
  ExceptionList = &local_10;
  local_14 = uVar1;
  DuiLib::CDuiString::CDuiString(local_14c);
  local_8 = 0;
  DuiLib::CDuiString::CDuiString(local_1d4);
  local_8._0_1_ = 1;
  pCVar2 = FUN_00401fb0(local_4b4);
  local_8._0_1_ = 2;
  DuiLib::CDuiString::operator=(local_14c,pCVar2);
  local_8 = CONCAT31(local_8._1_3_,1);
  DuiLib::CDuiString::~CDuiString(local_4b4);
  DuiLib::CDuiString::operator+=(local_14c,L"Data");
  lpFindFileData = &local_424;
  pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_14c);
  hFindFile = FindFirstFileW(pwVar3,lpFindFileData);
  FindClose(hFindFile);
  if ((hFindFile == (HANDLE)0xffffffff) || (((byte)local_424.dwFileAttributes & 0x10) == 0)) {
    lpSecurityAttributes = (LPSECURITY_ATTRIBUTES)0x0;
    pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_14c);
    CreateDirectoryW(pwVar3,lpSecurityAttributes);
  }
  pCVar2 = (CDuiString *)DuiLib::CDuiString::operator+(local_14c,(wchar_t *)local_4b4);
  local_8._0_1_ = 3;
  DuiLib::CDuiString::operator=(local_1d4,pCVar2);
  local_8._0_1_ = 1;
  DuiLib::CDuiString::~CDuiString(local_4b4);
  memset(&local_c4,0,0xb0);
  pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_1d4);
  FUN_00404ee0(&local_c4,pwVar3);
  local_8 = CONCAT31(local_8._1_3_,4);
  pbVar4 = std::basic_ostream<char,std::char_traits<char>_>::write
                     ((basic_ostream<char,std::char_traits<char>_> *)&local_c4,local_428,
                      (ulonglong)uVar1 << 0x20);
  if (((byte)pbVar4[*(int *)(*(int *)pbVar4 + 4) + 0xc] & 6) != 0) {
    GetLastError();
  }
  pbVar5 = FUN_004051d0((basic_streambuf<char,std::char_traits<char>_> *)&local_c0);
  if (pbVar5 == (basic_streambuf<char,std::char_traits<char>_> *)0x0) {
    std::basic_ios<char,std::char_traits<char>_>::setstate
              ((basic_ios<char,std::char_traits<char>_> *)
               (local_14c + *(int *)(local_c4 + 4) + 0x88),2,false);
  }
  *(undefined ***)(local_14c + *(int *)(local_c4 + 4) + 0x88) =
       std::basic_ofstream<char,std::char_traits<char>_>::vftable;
  *(int *)(local_14c + *(int *)(local_c4 + 4) + 0x84) = *(int *)(local_c4 + 4) + -0x68;
  local_8 = CONCAT31(local_8._1_3_,5);
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
  DuiLib::CDuiString::~CDuiString(local_1d4);
  DuiLib::CDuiString::~CDuiString(local_14c);
  ExceptionList = local_10;
  return 1;
}


