// Program: SM809 mouse Software.exe
// Function: FUN_0040db60
// Entry: 0040db60
// Body: 0040db60 - 0040de78
// Signature: undefined FUN_0040db60(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_0040db60(int param_1)

{
  uint uVar1;
  CDuiString *pCVar2;
  wchar_t *pwVar3;
  BOOL BVar4;
  int iVar5;
  basic_streambuf<char,std::char_traits<char>_> *pbVar6;
  CDuiString *this;
  code *pcVar7;
  int *piVar8;
  tagOFNW local_4b0;
  CDuiString local_458 [132];
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
  puStack_c = &LAB_00422380;
  local_10 = ExceptionList;
  uVar1 = DAT_00432008 ^ (uint)(local_21c + 0x10c);
  ExceptionList = &local_10;
  if (-1 < *(int *)(param_1 + 0x1a8)) {
    local_14 = uVar1;
    DuiLib::CDuiString::CDuiString(local_458);
    local_8 = 0;
    pCVar2 = DuiLib::CStdPtrArray::operator[]
                       ((CStdPtrArray *)(param_1 + 0x19c),*(int *)(param_1 + 0x1a8));
    pwVar3 = DuiLib::CDuiString::GetData(pCVar2);
    DuiLib::CDuiString::operator=(local_458,pwVar3);
    DuiLib::CDuiString::CDuiString(local_3d4);
    local_8._0_1_ = 1;
    DuiLib::CDuiString::CDuiString(local_350);
    local_8._0_1_ = 2;
    pCVar2 = FUN_00401fb0(local_2a0);
    local_8._0_1_ = 3;
    DuiLib::CDuiString::operator=(local_350,pCVar2);
    pcVar7 = ~CDuiString_exref;
    local_8._0_1_ = 2;
    DuiLib::CDuiString::~CDuiString(local_2a0);
    pwVar3 = DuiLib::CDuiString::GetData(local_350);
    DuiLib::CDuiString::Format(this,(wchar_t *)local_3d4,L"%Data",pwVar3);
    memset(&local_4b0,0,0x58);
    memset(local_21c,0,0x208);
    local_4b0.lStructSize = 0x58;
    local_4b0.lpstrFilter = L"Gun Data";
    local_4b0.nFilterIndex = 1;
    local_4b0.hwndOwner = *(HWND *)(param_1 + 0x14);
    local_4b0.lpstrFile = local_21c;
    local_4b0.nMaxFile = 0x208;
    local_4b0.lpstrInitialDir = DuiLib::CDuiString::operator_wchar_t_const_(local_3d4);
    local_4b0.Flags = 0x806;
    local_4b0.lpstrDefExt = L"gbins";
    BVar4 = GetSaveFileNameW(&local_4b0);
    if (BVar4 != 0) {
      memset(&local_2cc,0,0xb0);
      FUN_00404ee0(&local_2cc,local_4b0.lpstrFile);
      local_8 = CONCAT31(local_8._1_3_,4);
      piVar8 = DAT_0046c398;
      if (DAT_0046c398 != DAT_0046c39c) {
        do {
          pwVar3 = (wchar_t *)*piVar8;
          iVar5 = DuiLib::CDuiString::CompareNoCase(local_458,pwVar3);
          if (iVar5 == 0) {
            iVar5 = *(int *)(pwVar3 + 0x66);
            pwVar3[0x66] = L'\x01';
            pwVar3[0x67] = L'\0';
            std::basic_ostream<char,std::char_traits<char>_>::write
                      ((basic_ostream<char,std::char_traits<char>_> *)&local_2cc,(char *)pwVar3,
                       (ulonglong)uVar1 << 0x20);
            if (iVar5 != 1) {
              pwVar3[0x66] = L'\0';
              pwVar3[0x67] = L'\0';
            }
          }
          piVar8 = piVar8 + 1;
        } while (piVar8 != DAT_0046c39c);
        pcVar7 = ~CDuiString_exref;
      }
      pbVar6 = FUN_004051d0((basic_streambuf<char,std::char_traits<char>_> *)&local_2c8);
      if (pbVar6 == (basic_streambuf<char,std::char_traits<char>_> *)0x0) {
        std::basic_ios<char,std::char_traits<char>_>::setstate
                  ((basic_ios<char,std::char_traits<char>_> *)
                   (local_350 + *(int *)(local_2cc + 4) + 0x84),2,false);
      }
      *(undefined ***)(local_350 + *(int *)(local_2cc + 4) + 0x84) =
           std::basic_ofstream<char,std::char_traits<char>_>::vftable;
      *(int *)(local_350 + *(int *)(local_2cc + 4) + 0x80) = *(int *)(local_2cc + 4) + -0x68;
      local_8._0_1_ = 5;
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
    (*pcVar7)();
    (*pcVar7)();
    (*pcVar7)();
  }
  ExceptionList = local_10;
  return;
}


