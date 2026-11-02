// Program: SM809 mouse Software.exe
// Function: FUN_0041b850
// Entry: 0041b850
// Body: 0041b850 - 0041bbb0
// Signature: undefined4 FUN_0041b850(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

undefined4 __fastcall FUN_0041b850(int param_1)

{
  int iVar1;
  uint uVar2;
  CDuiString *pCVar3;
  wchar_t *lpFile;
  undefined4 *puVar4;
  undefined4 auStack_bc0 [23];
  undefined4 uStack_b64;
  LPCWSTR lpParameters;
  LPCWSTR lpDirectory;
  INT nShowCmd;
  CDuiString local_b30 [132];
  undefined **local_aac [4];
  undefined **local_a9c;
  undefined **local_a8c;
  undefined **local_a88;
  undefined **local_a84;
  undefined **local_a80;
  CDuiString local_330 [132];
  CDuiString local_2ac [132];
  CDuiString local_228 [132];
  WCHAR local_1a4 [100];
  byte local_dc [3];
  char local_d9;
  char local_d8;
  char local_d7;
  char local_d6;
  byte local_d5;
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_004236e8;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (int)register0x00000010 - 4U;
  ExceptionList = &local_10;
  memset(local_dc,0,200);
  local_dc[0] = 0x80;
  local_dc[1] = 0;
  local_d5 = ~(local_d6 + -0x80 + local_dc[2] + local_d9 + local_d8 + local_d7);
  if (*(int *)(param_1 + 0x1af0) != 0) {
    FUN_00414710(local_dc);
  }
  (**(code **)(param_1 + 0x788))();
  Sleep(0x1e);
  memset(local_dc + 2,0,0xc6);
  local_dc[0] = 0x80;
  local_dc[1] = 0;
  if (*(int *)(param_1 + 0x1af0) != 0) {
    FUN_00414710(local_dc);
  }
  iVar1 = (**(code **)(param_1 + 0x78c))();
  if (iVar1 != 0) {
    if (*(int *)(param_1 + 0x1af0) != 0) {
      FUN_00414810(local_dc);
    }
    wsprintfW(local_1a4,L"m_iVer_H: %02x, m_iVer_L: %02x, iVer_H: %02x, iVer_L: %02x\r\n");
    OutputDebugStringW(local_1a4);
    Sleep(0x1e);
    if ((DAT_00432ac4 != local_dc[1]) || (DAT_00432ac0 != local_dc[2])) {
      memset(local_aac,0,0x884);
      FUN_0041c1c0((WindowImplBase *)local_aac);
      local_8 = 0;
      DuiLib::CDuiString::operator=(local_330,L"warning_title_text");
      DuiLib::CDuiString::operator=(local_2ac,L"update_fw_text");
      uStack_b64 = 0x41ba34;
      DuiLib::CWindowWnd::Create
                ((CWindowWnd *)local_aac,(HWND__ *)0x0,L"MsgWnd",0x90000000,0x80,0,0,800,800,
                 (HMENU__ *)0x0);
      DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_aac);
      uVar2 = DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_aac);
      if (uVar2 == 1) {
        DuiLib::CDuiString::CDuiString(local_228);
        local_8._0_1_ = 1;
        pCVar3 = FUN_00401e90(local_b30);
        local_8._0_1_ = 2;
        puVar4 = auStack_bc0;
        for (iVar1 = 0x21; iVar1 != 0; iVar1 = iVar1 + -1) {
          *puVar4 = *(undefined4 *)pCVar3;
          pCVar3 = pCVar3 + 4;
          puVar4 = puVar4 + 1;
        }
        DuiLib::CDuiString::Format
                  ((CDuiString *)0x0,(wchar_t *)local_228,L"%s\\Update\\flashOnLine.exe");
        local_8 = CONCAT31(local_8._1_3_,1);
        DuiLib::CDuiString::~CDuiString(local_b30);
        nShowCmd = 5;
        lpDirectory = (LPCWSTR)0x0;
        lpParameters = (LPCWSTR)0x0;
        lpFile = DuiLib::CDuiString::operator_wchar_t_const_(local_228);
        ShellExecuteW((HWND)0x0,L"open",lpFile,lpParameters,lpDirectory,nShowCmd);
        DuiLib::CDuiString::~CDuiString(local_228);
        local_aac[0] = CMsgWnd::vftable;
        local_a9c = CMsgWnd::vftable;
        local_a8c = CMsgWnd::vftable;
        local_a88 = CMsgWnd::vftable;
        local_a84 = CMsgWnd::vftable;
        local_a80 = CMsgWnd::vftable;
        DuiLib::CDuiString::~CDuiString(local_2ac);
        DuiLib::CDuiString::~CDuiString(local_330);
        DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_aac);
        ExceptionList = local_10;
        return 0;
      }
      local_aac[0] = CMsgWnd::vftable;
      local_a9c = CMsgWnd::vftable;
      local_a8c = CMsgWnd::vftable;
      local_a88 = CMsgWnd::vftable;
      local_a84 = CMsgWnd::vftable;
      local_a80 = CMsgWnd::vftable;
      DuiLib::CDuiString::~CDuiString(local_2ac);
      DuiLib::CDuiString::~CDuiString(local_330);
      DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_aac);
    }
  }
  ExceptionList = local_10;
  return 1;
}


