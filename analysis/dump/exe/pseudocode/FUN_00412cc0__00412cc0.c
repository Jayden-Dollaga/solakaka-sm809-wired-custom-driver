// Program: SM809 mouse Software.exe
// Function: FUN_00412cc0
// Entry: 00412cc0
// Body: 00412cc0 - 00412f3c
// Signature: undefined FUN_00412cc0(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_00412cc0(int param_1)

{
  uint uVar1;
  CDuiString *pCVar2;
  wchar_t *pwVar3;
  BOOL BVar4;
  basic_streambuf<char,std::char_traits<char>_> *pbVar5;
  CDuiString *this;
  tagOFNW local_42c;
  CDuiString local_3d4 [132];
  CDuiString local_350 [128];
  CDuiString aCStack_2d0 [4];
  int local_2cc;
  undefined **local_2c8;
  basic_ostream<char,std::char_traits<char>_> local_2c4 [8];
  int *local_2bc;
  int *local_2ac;
  CDuiString local_2a0 [4];
  int *local_29c;
  undefined1 local_28c [12];
  char local_280;
  int local_27c;
  int local_278;
  int local_274;
  basic_ios<char,std::char_traits<char>_> local_264 [72];
  wchar_t local_21c [260];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00422064;
  local_10 = ExceptionList;
  uVar1 = DAT_00432008 ^ (uint)(local_21c + 0x10c);
  ExceptionList = &local_10;
  if (*(int *)(param_1 + 0x1c) != 0) {
    local_14 = uVar1;
    DuiLib::CDuiString::CDuiString(local_3d4);
    local_8 = 0;
    DuiLib::CDuiString::CDuiString(local_350);
    local_8._0_1_ = 1;
    pCVar2 = FUN_00401fb0(local_2a0);
    local_8._0_1_ = 2;
    DuiLib::CDuiString::operator=(local_350,pCVar2);
    local_8._0_1_ = 1;
    DuiLib::CDuiString::~CDuiString(local_2a0);
    pwVar3 = DuiLib::CDuiString::GetData(local_350);
    DuiLib::CDuiString::Format(this,(wchar_t *)local_3d4,L"%Data",pwVar3);
    memset(&local_42c,0,0x58);
    memset(local_21c,0,0x208);
    local_42c.hwndOwner = *(HWND *)(param_1 + 0x14);
    local_42c.lpstrFile = local_21c;
    local_42c.lStructSize = 0x58;
    local_42c.lpstrFilter = L"Macro Data";
    local_42c.nFilterIndex = 1;
    local_42c.nMaxFile = 0x208;
    local_42c.lpstrInitialDir = DuiLib::CDuiString::operator_wchar_t_const_(local_3d4);
    local_42c.Flags = 0x806;
    local_42c.lpstrDefExt = L"mbin";
    BVar4 = GetSaveFileNameW(&local_42c);
    if (BVar4 != 0) {
      memset(&local_2cc,0,0xb0);
      FUN_00404ee0(&local_2cc,local_42c.lpstrFile);
      local_8 = CONCAT31(local_8._1_3_,3);
      std::basic_ostream<char,std::char_traits<char>_>::write
                ((basic_ostream<char,std::char_traits<char>_> *)&local_2cc,
                 *(char **)(param_1 + 0x1c),(ulonglong)uVar1 << 0x20);
      pbVar5 = FUN_004051d0((basic_streambuf<char,std::char_traits<char>_> *)&local_2c8);
      if (pbVar5 == (basic_streambuf<char,std::char_traits<char>_> *)0x0) {
        std::basic_ios<char,std::char_traits<char>_>::setstate
                  ((basic_ios<char,std::char_traits<char>_> *)
                   (local_350 + *(int *)(local_2cc + 4) + 0x84),2,false);
      }
      *(undefined ***)(local_350 + *(int *)(local_2cc + 4) + 0x84) =
           std::basic_ofstream<char,std::char_traits<char>_>::vftable;
      *(int *)(local_350 + *(int *)(local_2cc + 4) + 0x80) = *(int *)(local_2cc + 4) + -0x68;
      local_8._0_1_ = 4;
      local_2c8 = std::basic_filebuf<char,std::char_traits<char>_>::vftable;
      if ((local_27c != 0) && ((undefined1 *)*local_2bc == local_28c)) {
        *local_2bc = local_278;
        *local_2ac = local_278;
        *local_29c = local_274 - local_278;
      }
      if (local_280 != '\0') {
        FUN_004051d0((basic_streambuf<char,std::char_traits<char>_> *)&local_2c8);
      }
      std::basic_streambuf<char,std::char_traits<char>_>::
      ~basic_streambuf<char,std::char_traits<char>_>
                ((basic_streambuf<char,std::char_traits<char>_> *)&local_2c8);
      std::basic_ostream<char,std::char_traits<char>_>::~basic_ostream<char,std::char_traits<char>_>
                (local_2c4);
      std::basic_ios<char,std::char_traits<char>_>::~basic_ios<char,std::char_traits<char>_>
                (local_264);
    }
    DuiLib::CDuiString::~CDuiString(local_350);
    DuiLib::CDuiString::~CDuiString(local_3d4);
  }
  ExceptionList = local_10;
  return;
}


