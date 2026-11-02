// Program: SM809 mouse Software.exe
// Function: FUN_004037f0
// Entry: 004037f0
// Body: 004037f0 - 004039d7
// Signature: undefined FUN_004037f0(void)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void FUN_004037f0(void)

{
  uint uVar1;
  CDuiString *pCVar2;
  wchar_t *pwVar3;
  int iVar4;
  char *pcVar5;
  basic_streambuf<char,std::char_traits<char>_> *pbVar6;
  undefined4 extraout_ECX;
  CDuiString local_2f4 [140];
  char *local_268;
  int local_264 [3];
  byte abStack_258 [4];
  basic_streambuf<char,std::char_traits<char>_> local_254 [168];
  CDuiString local_1ac [136];
  CDuiString local_124 [136];
  CDuiString local_9c [136];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  iVar4 = DAT_00432ad8;
  local_8 = 0xffffffff;
  puStack_c = &LAB_0042126c;
  local_10 = ExceptionList;
  uVar1 = DAT_00432008 ^ (uint)(local_9c + 0x98);
  ExceptionList = &local_10;
  local_14 = uVar1;
  DuiLib::CDuiString::CDuiString(local_124);
  local_8 = 0;
  DuiLib::CDuiString::CDuiString(local_1ac);
  local_8._0_1_ = 1;
  DuiLib::CDuiString::CDuiString(local_9c);
  local_8._0_1_ = 2;
  pCVar2 = FUN_00401fb0(local_2f4);
  local_8._0_1_ = 3;
  DuiLib::CDuiString::operator=(local_124,pCVar2);
  local_8._0_1_ = 2;
  DuiLib::CDuiString::~CDuiString(local_2f4);
  pCVar2 = (CDuiString *)DuiLib::CDuiString::operator+(local_124,(wchar_t *)local_2f4);
  local_8._0_1_ = 4;
  DuiLib::CDuiString::operator=(local_9c,pCVar2);
  local_8._0_1_ = 2;
  DuiLib::CDuiString::~CDuiString(local_2f4);
  memset(local_264,0,0xb8);
  pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_9c);
  FUN_00404320(local_264,pwVar3);
  local_8 = CONCAT31(local_8._1_3_,5);
  if ((abStack_258[*(int *)(local_264[0] + 4)] & 6) == 0) {
    iVar4 = std::basic_istream<char,std::char_traits<char>_>::peek
                      ((basic_istream<char,std::char_traits<char>_> *)local_264);
    while (iVar4 != -1) {
      pcVar5 = operator_new(0x1cc50);
      local_268 = pcVar5;
      std::basic_istream<char,std::char_traits<char>_>::read
                ((basic_istream<char,std::char_traits<char>_> *)local_264,pcVar5,
                 (ulonglong)uVar1 << 0x20);
      if (DAT_0046c390 == DAT_0046c394) {
        FUN_00405390(DAT_0046c390,&local_268);
      }
      else {
        *DAT_0046c390 = pcVar5;
        DAT_0046c390 = DAT_0046c390 + 1;
      }
      iVar4 = std::basic_istream<char,std::char_traits<char>_>::peek
                        ((basic_istream<char,std::char_traits<char>_> *)local_264);
    }
  }
  else {
    FUN_00403af0(extraout_ECX,iVar4);
  }
  pbVar6 = FUN_004051d0(local_254);
  if (pbVar6 == (basic_streambuf<char,std::char_traits<char>_> *)0x0) {
    std::basic_ios<char,std::char_traits<char>_>::setstate
              ((basic_ios<char,std::char_traits<char>_> *)
               ((int)local_264 + *(int *)(local_264[0] + 4)),2,false);
  }
  FUN_00402e30(local_264);
  DuiLib::CDuiString::~CDuiString(local_9c);
  DuiLib::CDuiString::~CDuiString(local_1ac);
  DuiLib::CDuiString::~CDuiString(local_124);
  ExceptionList = local_10;
  return;
}


