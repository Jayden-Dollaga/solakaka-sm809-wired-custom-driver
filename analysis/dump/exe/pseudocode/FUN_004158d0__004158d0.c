// Program: SM809 mouse Software.exe
// Function: FUN_004158d0
// Entry: 004158d0
// Body: 004158d0 - 00416c4a
// Signature: undefined FUN_004158d0(CWindowWnd * param_1)


/* WARNING: Function: __alloca_probe replaced with injection: alloca_probe */
/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_004158d0(CWindowWnd *param_1)

{
  wchar_t wVar1;
  uint uVar2;
  CDuiString *pCVar3;
  wchar_t *pwVar4;
  wchar_t *pwVar5;
  wchar_t *pwVar6;
  wchar_t *pwVar7;
  UINT UVar8;
  basic_streambuf<char,std::char_traits<char>_> *pbVar9;
  int iVar10;
  CWindowWnd *pCVar11;
  undefined4 uVar12;
  CResourceManager *pCVar13;
  CControlUI *pCVar14;
  HMODULE hModule;
  FARPROC pFVar15;
  CWindowWnd *pCVar16;
  code *pcVar17;
  char cVar18;
  WCHAR *pWVar19;
  DWORD DVar20;
  INT IVar21;
  undefined1 uVar22;
  CDuiString local_17d0 [132];
  CDuiString local_174c [132];
  CDuiString local_16c8 [132];
  HICON__ *local_1644;
  CDuiString *local_1640;
  CDuiString local_163c [132];
  CDuiString local_15b8 [132];
  CDuiString local_1534 [132];
  CDuiString local_14b0 [132];
  CDuiString local_142c [132];
  CDuiString local_13a8 [132];
  CDuiString local_1324 [128];
  CDuiString aCStack_12a4 [4];
  int local_12a0 [4];
  undefined **local_1290 [2];
  basic_istream<char,std::char_traits<char>_> local_1288 [4];
  int *local_1284;
  int *local_1274;
  int *local_1264;
  undefined1 local_1254 [12];
  char local_1248;
  int local_1244;
  int local_1240;
  int local_123c;
  basic_ios<char,std::char_traits<char>_> local_1230 [72];
  CDuiString local_11e8 [132];
  CDuiString local_1164 [132];
  CWindowWnd *local_10e0;
  WCHAR local_10dc [1982];
  CDuiString local_160 [132];
  WCHAR local_dc [100];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00423242;
  local_10 = ExceptionList;
  uVar2 = DAT_00432008 ^ (uint)(local_dc + 0x6c);
  ExceptionList = &local_10;
  uVar12 = *(undefined4 *)(param_1 + 4);
  pCVar16 = param_1 + 0x30;
  *(CWindowWnd **)(param_1 + 0x7b0) = pCVar16;
  *(CWindowWnd **)(param_1 + 0x970) = pCVar16;
  *(CWindowWnd **)(param_1 + 0xaa8) = pCVar16;
  *(CWindowWnd **)(param_1 + 0xb50) = pCVar16;
  *(CWindowWnd **)(param_1 + 0xf08) = pCVar16;
  *(undefined4 *)(param_1 + 0x7b4) = uVar12;
  *(undefined4 *)(param_1 + 0x974) = uVar12;
  *(undefined4 *)(param_1 + 0xaac) = uVar12;
  *(undefined4 *)(param_1 + 0xb54) = uVar12;
  *(undefined4 *)(param_1 + 0xf0c) = uVar12;
  local_10e0 = param_1;
  local_14 = uVar2;
  pCVar3 = FUN_00401e90(local_16c8);
  local_8 = 0;
  DuiLib::CDuiString::operator+(pCVar3,(wchar_t *)local_174c);
  local_8._0_1_ = 1;
  DuiLib::CDuiString::CDuiString(local_1324);
  local_8._0_1_ = 2;
  DuiLib::CDuiString::operator=(local_1324,local_174c);
  DuiLib::CDuiString::~CDuiString(local_174c);
  local_8._0_1_ = 4;
  DuiLib::CDuiString::~CDuiString(local_16c8);
  DuiLib::CDuiString::CDuiString(local_13a8);
  local_8._0_1_ = 5;
  DuiLib::CDuiString::CDuiString(local_1164,L"",-1);
  local_8._0_1_ = 6;
  DuiLib::CDuiString::CDuiString(local_11e8,L"VID",-1);
  local_8._0_1_ = 7;
  DuiLib::CDuiString::CDuiString(local_174c,L"Default",-1);
  local_8._0_1_ = 10;
  pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_1324);
  DVar20 = 0x1000;
  pWVar19 = local_10dc;
  pwVar5 = DuiLib::CDuiString::operator_wchar_t_const_(local_1164);
  pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_11e8);
  pwVar7 = DuiLib::CDuiString::operator_wchar_t_const_(local_174c);
  GetPrivateProfileStringW(pwVar7,pwVar6,pwVar5,pWVar19,DVar20,pwVar4);
  DuiLib::CDuiString::CDuiString(local_16c8,local_10dc,-1);
  DuiLib::CDuiString::~CDuiString(local_174c);
  DuiLib::CDuiString::~CDuiString(local_11e8);
  DuiLib::CDuiString::~CDuiString(local_1164);
  local_8._0_1_ = 0xb;
  DuiLib::CDuiString::operator=(local_13a8,local_16c8);
  local_8._0_1_ = 5;
  DuiLib::CDuiString::~CDuiString(local_16c8);
  uVar22 = 0x28;
  pwVar5 = L"%04x";
  pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_13a8);
  FUN_00405b80(pwVar4,pwVar5,uVar22);
  DuiLib::CDuiString::CDuiString(local_11e8,L"",-1);
  local_8._0_1_ = 0xc;
  DuiLib::CDuiString::CDuiString(local_174c,L"PID",-1);
  local_8._0_1_ = 0xd;
  DuiLib::CDuiString::CDuiString(local_16c8,L"Default",-1);
  local_8._0_1_ = 0x10;
  pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_1324);
  DVar20 = 0x1000;
  pWVar19 = local_10dc;
  pwVar5 = DuiLib::CDuiString::operator_wchar_t_const_(local_11e8);
  pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_174c);
  pwVar7 = DuiLib::CDuiString::operator_wchar_t_const_(local_16c8);
  GetPrivateProfileStringW(pwVar7,pwVar6,pwVar5,pWVar19,DVar20,pwVar4);
  DuiLib::CDuiString::CDuiString(local_1164,local_10dc,-1);
  DuiLib::CDuiString::~CDuiString(local_16c8);
  DuiLib::CDuiString::~CDuiString(local_174c);
  DuiLib::CDuiString::~CDuiString(local_11e8);
  local_8._0_1_ = 0x11;
  DuiLib::CDuiString::operator=(local_13a8,local_1164);
  local_8._0_1_ = 5;
  DuiLib::CDuiString::~CDuiString(local_1164);
  uVar22 = 0x2c;
  pwVar5 = L"%04x";
  pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_13a8);
  FUN_00405b80(pwVar4,pwVar5,uVar22);
  DuiLib::CDuiString::CDuiString(local_174c,L"DPI",-1);
  local_8._0_1_ = 0x12;
  DuiLib::CDuiString::CDuiString(local_16c8,L"Default",-1);
  local_8._0_1_ = 0x14;
  pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_1324);
  IVar21 = -1;
  pwVar5 = DuiLib::CDuiString::operator_wchar_t_const_(local_174c);
  pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_16c8);
  GetPrivateProfileIntW(pwVar6,pwVar5,IVar21,pwVar4);
  DuiLib::CDuiString::~CDuiString(local_16c8);
  local_8._0_1_ = 5;
  DuiLib::CDuiString::~CDuiString(local_174c);
  DuiLib::CDuiString::CDuiString(local_174c,L"Sensor",-1);
  local_8._0_1_ = 0x15;
  DuiLib::CDuiString::CDuiString(local_16c8,L"Default",-1);
  local_8._0_1_ = 0x17;
  pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_1324);
  IVar21 = -1;
  pwVar5 = DuiLib::CDuiString::operator_wchar_t_const_(local_174c);
  pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_16c8);
  UVar8 = GetPrivateProfileIntW(pwVar6,pwVar5,IVar21,pwVar4);
  DuiLib::CDuiString::~CDuiString(local_16c8);
  local_8._0_1_ = 5;
  DuiLib::CDuiString::~CDuiString(local_174c);
  DAT_00432ad8 = UVar8;
  DuiLib::CDuiString::CDuiString(local_174c,L"Distance",-1);
  local_8._0_1_ = 0x18;
  DuiLib::CDuiString::CDuiString(local_16c8,L"Default",-1);
  local_8._0_1_ = 0x1a;
  pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_1324);
  IVar21 = -1;
  pwVar5 = DuiLib::CDuiString::operator_wchar_t_const_(local_174c);
  pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_16c8);
  UVar8 = GetPrivateProfileIntW(pwVar6,pwVar5,IVar21,pwVar4);
  DuiLib::CDuiString::~CDuiString(local_16c8);
  local_8._0_1_ = 5;
  DuiLib::CDuiString::~CDuiString(local_174c);
  DAT_00432acc = UVar8;
  DuiLib::CDuiString::CDuiString(local_11e8,L"",-1);
  local_8._0_1_ = 0x1b;
  DuiLib::CDuiString::CDuiString(local_174c,L"Distance_Min",-1);
  local_8._0_1_ = 0x1c;
  DuiLib::CDuiString::CDuiString(local_16c8,L"Default",-1);
  local_8._0_1_ = 0x1f;
  pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_1324);
  DVar20 = 0x1000;
  pWVar19 = local_10dc;
  pwVar5 = DuiLib::CDuiString::operator_wchar_t_const_(local_11e8);
  pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_174c);
  pwVar7 = DuiLib::CDuiString::operator_wchar_t_const_(local_16c8);
  GetPrivateProfileStringW(pwVar7,pwVar6,pwVar5,pWVar19,DVar20,pwVar4);
  DuiLib::CDuiString::CDuiString(local_1164,local_10dc,-1);
  DuiLib::CDuiString::~CDuiString(local_16c8);
  DuiLib::CDuiString::~CDuiString(local_174c);
  DuiLib::CDuiString::~CDuiString(local_11e8);
  local_8._0_1_ = 0x20;
  DuiLib::CDuiString::operator=(local_13a8,local_1164);
  local_8._0_1_ = 5;
  DuiLib::CDuiString::~CDuiString(local_1164);
  uVar22 = 0xd4;
  pwVar5 = L"%02x";
  pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_13a8);
  FUN_00405b80(pwVar4,pwVar5,uVar22);
  DuiLib::CDuiString::CDuiString(local_11e8,L"",-1);
  local_8._0_1_ = 0x21;
  DuiLib::CDuiString::CDuiString(local_174c,L"Distance_Max",-1);
  local_8._0_1_ = 0x22;
  DuiLib::CDuiString::CDuiString(local_16c8,L"Default",-1);
  local_8._0_1_ = 0x25;
  pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_1324);
  DVar20 = 0x1000;
  pWVar19 = local_10dc;
  pwVar5 = DuiLib::CDuiString::operator_wchar_t_const_(local_11e8);
  pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_174c);
  pwVar7 = DuiLib::CDuiString::operator_wchar_t_const_(local_16c8);
  GetPrivateProfileStringW(pwVar7,pwVar6,pwVar5,pWVar19,DVar20,pwVar4);
  DuiLib::CDuiString::CDuiString(local_1164,local_10dc,-1);
  DuiLib::CDuiString::~CDuiString(local_16c8);
  DuiLib::CDuiString::~CDuiString(local_174c);
  DuiLib::CDuiString::~CDuiString(local_11e8);
  local_8._0_1_ = 0x26;
  DuiLib::CDuiString::operator=(local_13a8,local_1164);
  local_8._0_1_ = 5;
  DuiLib::CDuiString::~CDuiString(local_1164);
  uVar22 = 0xd0;
  pwVar5 = L"%02x";
  pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_13a8);
  FUN_00405b80(pwVar4,pwVar5,uVar22);
  DuiLib::CDuiString::CDuiString(local_163c);
  pCVar16 = param_1 + 0x158b;
  local_8._0_1_ = 0x27;
  local_1640 = (CDuiString *)0x0;
  do {
    local_1640 = local_1640 + 1;
    DuiLib::CDuiString::Format(local_1640,(wchar_t *)local_13a8,&DAT_00424f54,local_1640);
    DuiLib::CDuiString::CDuiString(local_11e8,L"",-1);
    local_8._0_1_ = 0x28;
    DuiLib::CDuiString::CDuiString(local_174c,local_13a8);
    local_8._0_1_ = 0x29;
    DuiLib::CDuiString::CDuiString(local_16c8,L"BUTTON",-1);
    local_8._0_1_ = 0x2c;
    pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_1324);
    DVar20 = 0x1000;
    pWVar19 = local_10dc;
    pwVar5 = DuiLib::CDuiString::operator_wchar_t_const_(local_11e8);
    pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_174c);
    pwVar7 = DuiLib::CDuiString::operator_wchar_t_const_(local_16c8);
    GetPrivateProfileStringW(pwVar7,pwVar6,pwVar5,pWVar19,DVar20,pwVar4);
    DuiLib::CDuiString::CDuiString(local_1164,local_10dc,-1);
    DuiLib::CDuiString::~CDuiString(local_16c8);
    DuiLib::CDuiString::~CDuiString(local_174c);
    DuiLib::CDuiString::~CDuiString(local_11e8);
    local_8._0_1_ = 0x2d;
    DuiLib::CDuiString::operator=(local_163c,local_1164);
    local_8._0_1_ = 0x27;
    DuiLib::CDuiString::~CDuiString(local_1164);
    DuiLib::CDuiString::CDuiString(local_16c8,local_163c);
    local_8._0_1_ = 0x2e;
    cVar18 = (char)pCVar16 + -3;
    pwVar5 = L"%02x,%02x,%02x,%02x,%02x";
    pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_16c8);
    FUN_00405b80(pwVar4,pwVar5,cVar18);
    local_8._0_1_ = 0x27;
    DuiLib::CDuiString::~CDuiString(local_16c8);
    pCVar16 = pCVar16 + 5;
  } while ((int)local_1640 < 0x40);
  DuiLib::CDuiString::CDuiString(local_14b0);
  local_8._0_1_ = 0x2f;
  pCVar3 = FUN_00401e90(local_174c);
  local_8._0_1_ = 0x30;
  pCVar3 = (CDuiString *)DuiLib::CDuiString::operator+(pCVar3,(wchar_t *)local_16c8);
  local_8._0_1_ = 0x31;
  DuiLib::CDuiString::operator=(local_14b0,pCVar3);
  DuiLib::CDuiString::~CDuiString(local_16c8);
  local_8._0_1_ = 0x2f;
  DuiLib::CDuiString::~CDuiString(local_174c);
  memset(local_12a0,0,0xb8);
  pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_14b0);
  FUN_00404320(local_12a0,pwVar4);
  local_8 = CONCAT31(local_8._1_3_,0x32);
  std::basic_istream<char,std::char_traits<char>_>::read
            ((basic_istream<char,std::char_traits<char>_> *)local_12a0,&DAT_00432ae0,
             (ulonglong)uVar2 << 0x20);
  pbVar9 = FUN_004051d0((basic_streambuf<char,std::char_traits<char>_> *)local_1290);
  pCVar16 = local_10e0;
  if (pbVar9 == (basic_streambuf<char,std::char_traits<char>_> *)0x0) {
    std::basic_ios<char,std::char_traits<char>_>::setstate
              ((basic_ios<char,std::char_traits<char>_> *)
               ((int)local_12a0 + *(int *)(local_12a0[0] + 4)),2,false);
  }
  DuiLib::CDuiString::CDuiString(local_142c);
  local_8._0_1_ = 0x33;
  DuiLib::CDuiString::CDuiString(local_11e8,L"",-1);
  local_8._0_1_ = 0x34;
  DuiLib::CDuiString::CDuiString(local_174c,L"Password",-1);
  local_8._0_1_ = 0x35;
  DuiLib::CDuiString::CDuiString(local_16c8,L"Default",-1);
  local_8._0_1_ = 0x38;
  pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_1324);
  DVar20 = 0x1000;
  pWVar19 = local_10dc;
  pwVar5 = DuiLib::CDuiString::operator_wchar_t_const_(local_11e8);
  pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_174c);
  pwVar7 = DuiLib::CDuiString::operator_wchar_t_const_(local_16c8);
  GetPrivateProfileStringW(pwVar7,pwVar6,pwVar5,pWVar19,DVar20,pwVar4);
  DuiLib::CDuiString::CDuiString(local_1164,local_10dc,-1);
  DuiLib::CDuiString::~CDuiString(local_16c8);
  DuiLib::CDuiString::~CDuiString(local_174c);
  DuiLib::CDuiString::~CDuiString(local_11e8);
  local_8._0_1_ = 0x39;
  DuiLib::CDuiString::operator=(local_142c,local_1164);
  local_8 = CONCAT31(local_8._1_3_,0x33);
  DuiLib::CDuiString::~CDuiString(local_1164);
  iVar10 = DuiLib::CDuiString::GetLength(local_142c);
  if (iVar10 == 6) {
    *(undefined4 *)(pCVar16 + 0x1af0) = 1;
    wVar1 = DuiLib::CDuiString::GetAt(local_142c,0);
    DAT_00432ab1 = (undefined1)wVar1;
    wVar1 = DuiLib::CDuiString::GetAt(local_142c,1);
    DAT_00432ab2 = (undefined1)wVar1;
    wVar1 = DuiLib::CDuiString::GetAt(local_142c,2);
    DAT_00432ab3 = (undefined1)wVar1;
    wVar1 = DuiLib::CDuiString::GetAt(local_142c,3);
    DAT_00432ab4 = (undefined1)wVar1;
    wVar1 = DuiLib::CDuiString::GetAt(local_142c,4);
    DAT_00432ab5 = (undefined1)wVar1;
    wVar1 = DuiLib::CDuiString::GetAt(local_142c,5);
    DAT_00432ab6 = (undefined1)wVar1;
  }
  else {
    *(undefined4 *)(pCVar16 + 0x1af0) = 0;
  }
  DuiLib::CDuiString::CDuiString(local_174c,L"Ver_H",-1);
  local_8._0_1_ = 0x3a;
  DuiLib::CDuiString::CDuiString(local_16c8,L"Default",-1);
  local_8._0_1_ = 0x3c;
  pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_1324);
  IVar21 = -1;
  pwVar5 = DuiLib::CDuiString::operator_wchar_t_const_(local_174c);
  pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_16c8);
  UVar8 = GetPrivateProfileIntW(pwVar6,pwVar5,IVar21,pwVar4);
  DuiLib::CDuiString::~CDuiString(local_16c8);
  local_8._0_1_ = 0x33;
  DuiLib::CDuiString::~CDuiString(local_174c);
  DAT_00432ac4 = UVar8;
  DuiLib::CDuiString::CDuiString(local_174c,L"Ver_L",-1);
  local_8._0_1_ = 0x3d;
  DuiLib::CDuiString::CDuiString(local_16c8,L"Default",-1);
  local_8._0_1_ = 0x3f;
  pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_1324);
  IVar21 = -1;
  pwVar5 = DuiLib::CDuiString::operator_wchar_t_const_(local_174c);
  pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_16c8);
  UVar8 = GetPrivateProfileIntW(pwVar6,pwVar5,IVar21,pwVar4);
  DuiLib::CDuiString::~CDuiString(local_16c8);
  local_8._0_1_ = 0x33;
  DuiLib::CDuiString::~CDuiString(local_174c);
  DAT_00432ac0 = UVar8;
  wsprintfW(local_dc,L"m_iVer_H_: %02x, m_iVer_L_: %02x\r\n",DAT_00432ac4,UVar8);
  OutputDebugStringW(local_dc);
  DuiLib::CDuiString::CDuiString(local_174c,L"Update",-1);
  local_8._0_1_ = 0x40;
  DuiLib::CDuiString::CDuiString(local_16c8,L"Default",-1);
  local_8._0_1_ = 0x42;
  pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_1324);
  IVar21 = -1;
  pwVar5 = DuiLib::CDuiString::operator_wchar_t_const_(local_174c);
  pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_16c8);
  UVar8 = GetPrivateProfileIntW(pwVar6,pwVar5,IVar21,pwVar4);
  DuiLib::CDuiString::~CDuiString(local_16c8);
  local_8._0_1_ = 0x33;
  DuiLib::CDuiString::~CDuiString(local_174c);
  DAT_00432abc = (uint)(UVar8 != 0);
  DuiLib::CDuiString::CDuiString(local_15b8);
  local_8._0_1_ = 0x43;
  DuiLib::CDuiString::CDuiString(local_11e8,L"",-1);
  local_8._0_1_ = 0x44;
  DuiLib::CDuiString::CDuiString(local_174c,L"Distance_Value",-1);
  local_8._0_1_ = 0x45;
  DuiLib::CDuiString::CDuiString(local_16c8,L"Default",-1);
  local_8._0_1_ = 0x48;
  pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_1324);
  DVar20 = 0x1000;
  pWVar19 = local_10dc;
  pwVar5 = DuiLib::CDuiString::operator_wchar_t_const_(local_11e8);
  pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_174c);
  pwVar7 = DuiLib::CDuiString::operator_wchar_t_const_(local_16c8);
  GetPrivateProfileStringW(pwVar7,pwVar6,pwVar5,pWVar19,DVar20,pwVar4);
  DuiLib::CDuiString::CDuiString(local_1164,local_10dc,-1);
  DuiLib::CDuiString::~CDuiString(local_16c8);
  DuiLib::CDuiString::~CDuiString(local_174c);
  DuiLib::CDuiString::~CDuiString(local_11e8);
  local_8._0_1_ = 0x49;
  DuiLib::CDuiString::operator=(local_15b8,local_1164);
  local_8._0_1_ = 0x43;
  DuiLib::CDuiString::~CDuiString(local_1164);
  cVar18 = (char)pCVar16 + -0x38;
  DuiLib::CDuiString::CDuiString(local_16c8,local_15b8);
  local_8._0_1_ = 0x4a;
  pwVar5 = L"%d,%d,%d,%d,%d,%d,%d,%d";
  pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_16c8);
  FUN_00405b80(pwVar4,pwVar5,cVar18);
  local_8._0_1_ = 0x43;
  DuiLib::CDuiString::~CDuiString(local_16c8);
  pCVar3 = FUN_00401e90(local_17d0);
  local_8._0_1_ = 0x4b;
  pCVar3 = (CDuiString *)DuiLib::CDuiString::operator+(pCVar3,(wchar_t *)local_16c8);
  local_8._0_1_ = 0x4c;
  DuiLib::CDuiString::operator=(local_14b0,pCVar3);
  DuiLib::CDuiString::~CDuiString(local_16c8);
  DuiLib::CDuiString::~CDuiString(local_17d0);
  pCVar11 = (CWindowWnd *)GdipAlloc(0x10);
  local_8._0_1_ = 0x4d;
  if (pCVar11 == (CWindowWnd *)0x0) {
    pCVar11 = (CWindowWnd *)0x0;
  }
  else {
    *(undefined4 *)pCVar11 = 0;
    *(undefined4 *)(pCVar11 + 4) = 0;
    *(undefined4 *)(pCVar11 + 8) = 0;
    *(undefined4 *)(pCVar11 + 0xc) = 0;
    local_10e0 = pCVar11;
    pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_14b0);
    *(undefined ***)pCVar11 = Gdiplus::Bitmap::vftable;
    local_1640 = (CDuiString *)0x0;
    uVar12 = GdipCreateBitmapFromFile(pwVar4,&local_1640);
    *(undefined4 *)(pCVar11 + 8) = uVar12;
    *(CDuiString **)(pCVar11 + 4) = local_1640;
  }
  local_8._0_1_ = 0x43;
  local_10e0 = (CWindowWnd *)0x0;
  iVar10 = GdipGetImageHeight(*(undefined4 *)(pCVar11 + 4),&local_10e0);
  if (iVar10 != 0) {
    *(int *)(pCVar11 + 8) = iVar10;
  }
  local_1644 = (HICON__ *)0x0;
  iVar10 = GdipCreateHICONFromBitmap(*(undefined4 *)(pCVar11 + 4),&local_1644);
  if (iVar10 != 0) {
    *(int *)(pCVar11 + 8) = iVar10;
  }
  DuiLib::CWindowWnd::SendMessageW(pCVar16,0x80,1,(long)local_1644);
  DuiLib::CWindowWnd::SendMessageW(pCVar16,0x80,0,(long)local_1644);
  pCVar13 = DuiLib::CResourceManager::GetInstance();
  pwVar4 = L"Language/lan.xml";
  *(uint *)(pCVar13 + 0xc) = -(uint)(pCVar16 != (CWindowWnd *)0x0) & (uint)(pCVar16 + 0x2c);
  pCVar13 = DuiLib::CResourceManager::GetInstance();
  DuiLib::CResourceManager::LoadLanguage(pCVar13,pwVar4);
  pCVar3 = local_17d0;
  pwVar4 = L"mouse_name_text";
  pCVar13 = DuiLib::CResourceManager::GetInstance();
  pCVar3 = (CDuiString *)DuiLib::CResourceManager::GetText(pCVar13,(wchar_t *)pCVar3,pwVar4);
  local_8._0_1_ = 0x4e;
  DuiLib::CDuiString::operator=(local_14b0,pCVar3);
  local_8._0_1_ = 0x43;
  DuiLib::CDuiString::~CDuiString(local_17d0);
  pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_14b0);
  SetWindowTextW(*(HWND *)(pCVar16 + 4),pwVar4);
  pCVar14 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(pCVar16 + 0x30),L"exit_btn");
  *(CControlUI **)(pCVar16 + 0x16dc) = pCVar14;
  pCVar14 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(pCVar16 + 0x30),L"min_btn");
  *(CControlUI **)(pCVar16 + 0x16e0) = pCVar14;
  pCVar14 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(pCVar16 + 0x30),L"skin_btn");
  *(CControlUI **)(pCVar16 + 0x16d4) = pCVar14;
  pCVar14 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(pCVar16 + 0x30),L"setting_btn")
  ;
  *(CControlUI **)(pCVar16 + 0x16d8) = pCVar14;
  pCVar14 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(pCVar16 + 0x30),L"logo_btn");
  *(CControlUI **)(pCVar16 + 0x16e4) = pCVar14;
  pCVar14 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(pCVar16 + 0x30),L"key_btn");
  *(CControlUI **)(pCVar16 + 0x16e8) = pCVar14;
  pCVar14 = DuiLib::CPaintManagerUI::FindControl
                      ((CPaintManagerUI *)(pCVar16 + 0x30),L"performance_btn");
  *(CControlUI **)(pCVar16 + 0x16ec) = pCVar14;
  pCVar14 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(pCVar16 + 0x30),L"light_btn");
  *(CControlUI **)(pCVar16 + 0x16f0) = pCVar14;
  pCVar14 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(pCVar16 + 0x30),L"macro_btn");
  *(CControlUI **)(pCVar16 + 0x16f4) = pCVar14;
  pCVar14 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(pCVar16 + 0x30),L"gun_btn");
  *(CControlUI **)(pCVar16 + 0x16f8) = pCVar14;
  pCVar14 = DuiLib::CPaintManagerUI::FindControl
                      ((CPaintManagerUI *)(pCVar16 + 0x30),L"profile_combo");
  *(CControlUI **)(pCVar16 + 0x16fc) = pCVar14;
  pCVar14 = DuiLib::CPaintManagerUI::FindControl
                      ((CPaintManagerUI *)(pCVar16 + 0x30),L"btn_add_profile");
  *(CControlUI **)(pCVar16 + 0x1700) = pCVar14;
  pCVar14 = DuiLib::CPaintManagerUI::FindControl
                      ((CPaintManagerUI *)(pCVar16 + 0x30),L"btn_delete_profile");
  *(CControlUI **)(pCVar16 + 0x1704) = pCVar14;
  pCVar14 = DuiLib::CPaintManagerUI::FindControl
                      ((CPaintManagerUI *)(pCVar16 + 0x30),L"btn_menu_profile");
  *(CControlUI **)(pCVar16 + 0x1708) = pCVar14;
  pCVar14 = DuiLib::CPaintManagerUI::FindControl
                      ((CPaintManagerUI *)(pCVar16 + 0x30),L"edit_profile_name");
  *(CControlUI **)(pCVar16 + 0x170c) = pCVar14;
  pCVar14 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(pCVar16 + 0x30),L"btn_apply");
  *(CControlUI **)(pCVar16 + 0x1714) = pCVar14;
  pCVar14 = DuiLib::CPaintManagerUI::FindControl
                      ((CPaintManagerUI *)(pCVar16 + 0x30),L"btn_reset_profile");
  *(CControlUI **)(pCVar16 + 0x1710) = pCVar14;
  pCVar14 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(pCVar16 + 0x30),L"config_tab");
  *(CControlUI **)(pCVar16 + 0x1718) = pCVar14;
  pCVar14 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(pCVar16 + 0x30),L"main_tab");
  *(CControlUI **)(pCVar16 + 0x171c) = pCVar14;
  DuiLib::CDuiString::CDuiString(local_1534);
  pCVar3 = local_17d0;
  local_8._0_1_ = 0x4f;
  pwVar4 = L"mouse_name_text";
  pCVar13 = DuiLib::CResourceManager::GetInstance();
  pCVar3 = (CDuiString *)DuiLib::CResourceManager::GetText(pCVar13,(wchar_t *)pCVar3,pwVar4);
  local_8._0_1_ = 0x50;
  DuiLib::CDuiString::operator=(local_1534,pCVar3);
  pcVar17 = ~CDuiString_exref;
  local_8._0_1_ = 0x4f;
  DuiLib::CDuiString::~CDuiString(local_17d0);
  uVar2 = 0;
  pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_1534);
  DuiLib::CTrayIcon::CreateTrayIcon
            ((CTrayIcon *)(pCVar16 + 0x1724),*(HWND__ **)(pCVar16 + 4),local_1644,pwVar4,uVar2);
  (**(code **)(*(int *)(pCVar16 + 0x7a0) + 4))();
  (**(code **)(*(int *)(pCVar16 + 0x960) + 4))();
  (**(code **)(*(int *)(pCVar16 + 0xa98) + 4))();
  (**(code **)(*(int *)(pCVar16 + 0xb40) + 4))();
  (**(code **)(*(int *)(pCVar16 + 0xef8) + 4))();
  FUN_00416c70((int)pCVar16);
  CreateThread((LPSECURITY_ATTRIBUTES)0x0,0x1000,FUN_00414910,pCVar16,0,&DAT_00432ab8);
  DuiLib::CDuiString::CDuiString(local_11e8);
  local_8._0_1_ = 0x51;
  DuiLib::CDuiString::CDuiString(local_1164);
  local_8._0_1_ = 0x52;
  pCVar3 = FUN_00401e90(local_16c8);
  local_8._0_1_ = 0x53;
  DuiLib::CDuiString::operator=(local_11e8,pCVar3);
  local_8._0_1_ = 0x52;
  DuiLib::CDuiString::~CDuiString(local_16c8);
  pCVar3 = (CDuiString *)DuiLib::CDuiString::operator+(local_11e8,(wchar_t *)local_160);
  local_8._0_1_ = 0x54;
  DuiLib::CDuiString::operator=(local_1164,pCVar3);
  local_8 = CONCAT31(local_8._1_3_,0x52);
  DuiLib::CDuiString::~CDuiString(local_160);
  pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_1164);
  hModule = LoadLibraryW(pwVar4);
  *(HMODULE *)(pCVar16 + 0x1584) = hModule;
  if (hModule != (HMODULE)0x0) {
    pFVar15 = GetProcAddress(hModule,"Set_VIDPID");
    *(FARPROC *)(pCVar16 + 0x774) = pFVar15;
    pFVar15 = GetProcAddress(*(HMODULE *)(pCVar16 + 0x1584),"Open_DevMonitor");
    *(FARPROC *)(pCVar16 + 0x778) = pFVar15;
    pFVar15 = GetProcAddress(*(HMODULE *)(pCVar16 + 0x1584),"Close_DevMonitor");
    *(FARPROC *)(pCVar16 + 0x77c) = pFVar15;
    pFVar15 = GetProcAddress(*(HMODULE *)(pCVar16 + 0x1584),"Open_FeatureDevice");
    *(FARPROC *)(pCVar16 + 0x780) = pFVar15;
    pFVar15 = GetProcAddress(*(HMODULE *)(pCVar16 + 0x1584),"Close_FeatureDevice");
    *(FARPROC *)(pCVar16 + 0x784) = pFVar15;
    pFVar15 = GetProcAddress(*(HMODULE *)(pCVar16 + 0x1584),"SetFeature");
    *(FARPROC *)(pCVar16 + 0x788) = pFVar15;
    pFVar15 = GetProcAddress(*(HMODULE *)(pCVar16 + 0x1584),"GetFeature");
    *(FARPROC *)(pCVar16 + 0x78c) = pFVar15;
    pFVar15 = GetProcAddress(*(HMODULE *)(pCVar16 + 0x1584),"Open_ReportDevice");
    *(FARPROC *)(pCVar16 + 0x790) = pFVar15;
    pFVar15 = GetProcAddress(*(HMODULE *)(pCVar16 + 0x1584),"Close_ReportDevice");
    *(FARPROC *)(pCVar16 + 0x794) = pFVar15;
    pFVar15 = GetProcAddress(*(HMODULE *)(pCVar16 + 0x1584),"WriteUSB");
    *(FARPROC *)(pCVar16 + 0x798) = pFVar15;
    pFVar15 = GetProcAddress(*(HMODULE *)(pCVar16 + 0x1584),"ReadUSB");
    pcVar17 = ~CDuiString_exref;
    *(FARPROC *)(pCVar16 + 0x79c) = pFVar15;
  }
  (*pcVar17)();
  local_8 = CONCAT31(local_8._1_3_,0x4f);
  (*pcVar17)();
  (**(code **)(pCVar16 + 0x774))(DAT_00432028,DAT_0043202c);
  (**(code **)(pCVar16 + 0x778))(*(undefined4 *)(pCVar16 + 4),0x52d,0x52e);
  (**(code **)(pCVar16 + 0x780))();
  iVar10 = (**(code **)(pCVar16 + 0x790))();
  *(undefined4 *)(pCVar16 + 0x16d0) = 1;
  if (iVar10 == 0) {
    DAT_00432aa4 = 0;
  }
  else {
    DAT_00432aa4 = 1;
    FUN_004196b0((int)pCVar16);
    FUN_0041bbc0((int)pCVar16);
    if ((*(int *)(pCVar16 + 0x16d0) != 0) && (DAT_00432abc != 0)) {
      iVar10 = FUN_0041b850((int)pCVar16);
      if (iVar10 == 0) {
        DestroyWindow(*(HWND *)(pCVar16 + 4));
      }
    }
  }
  (*pcVar17)();
  (*pcVar17)();
  (*pcVar17)();
  *(undefined ***)((int)local_12a0 + *(int *)(local_12a0[0] + 4)) =
       std::basic_ifstream<char,std::char_traits<char>_>::vftable;
  *(int *)(local_1324 + *(int *)(local_12a0[0] + 4) + 0x80) = *(int *)(local_12a0[0] + 4) + -0x70;
  local_8 = CONCAT31(local_8._1_3_,0x55);
  local_1290[0] = std::basic_filebuf<char,std::char_traits<char>_>::vftable;
  if ((local_1244 != 0) && ((undefined1 *)*local_1284 == local_1254)) {
    *local_1284 = local_1240;
    *local_1274 = local_1240;
    *local_1264 = local_123c - local_1240;
  }
  if (local_1248 != '\0') {
    FUN_004051d0((basic_streambuf<char,std::char_traits<char>_> *)local_1290);
  }
  std::basic_streambuf<char,std::char_traits<char>_>::~basic_streambuf<char,std::char_traits<char>_>
            ((basic_streambuf<char,std::char_traits<char>_> *)local_1290);
  std::basic_istream<char,std::char_traits<char>_>::~basic_istream<char,std::char_traits<char>_>
            (local_1288);
  std::basic_ios<char,std::char_traits<char>_>::~basic_ios<char,std::char_traits<char>_>(local_1230)
  ;
  (*pcVar17)();
  (*pcVar17)();
  (*pcVar17)();
  (*pcVar17)();
  ExceptionList = local_10;
  return;
}


