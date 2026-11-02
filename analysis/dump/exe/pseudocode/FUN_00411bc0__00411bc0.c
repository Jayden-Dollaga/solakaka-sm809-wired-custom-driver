// Program: SM809 mouse Software.exe
// Function: FUN_00411bc0
// Entry: 00411bc0
// Body: 00411bc0 - 00411dfe
// Signature: undefined FUN_00411bc0(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_00411bc0(int param_1)

{
  undefined4 *puVar1;
  int iVar2;
  uint uVar3;
  CControlUI *pCVar4;
  wchar_t *pwVar5;
  undefined4 uVar6;
  int *piVar7;
  undefined **local_a30 [4];
  undefined **local_a20;
  undefined **local_a10;
  undefined **local_a0c;
  undefined **local_a08;
  undefined **local_a04;
  CDuiString local_2c8 [132];
  CDuiString local_244 [132];
  undefined4 *local_1c0;
  CDuiString local_1bc [132];
  CDuiString local_138 [132];
  undefined4 local_b4;
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00422a8c;
  local_10 = ExceptionList;
  uVar3 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  if (-1 < *(int *)(param_1 + 0x314)) {
    local_14 = uVar3;
    DuiLib::CDuiString::CDuiString(local_98);
    local_8 = 0;
    DuiLib::CDuiString::operator=(local_98,(wchar_t *)(*(int *)(param_1 + 0x1c) + 100));
    pCVar4 = DuiLib::CPaintManagerUI::FindControl
                       (*(CPaintManagerUI **)(param_1 + 0x10),L"disable_window_ver");
    (**(code **)(*(int *)pCVar4 + 0xf8))(1,uVar3);
    memset(local_a30,0,0x998);
    FUN_00409940((WindowImplBase *)local_a30);
    local_8 = CONCAT31(local_8._1_3_,1);
    DuiLib::CDuiString::operator=(local_138,local_98);
    DuiLib::CDuiString::operator=(local_1bc,*(wchar_t **)(param_1 + 0x1c));
    local_b4 = 3;
    local_1c0 = &DAT_0046c380;
    DuiLib::CWindowWnd::Create
              ((CWindowWnd *)local_a30,*(HWND__ **)(param_1 + 0x14),L"EditMacroName",0x90000000,0x80
               ,0,0,800,800,(HMENU__ *)0x0);
    DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_a30);
    uVar3 = DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_a30);
    if (uVar3 == 1) {
      pwVar5 = DuiLib::CDuiString::operator_wchar_t_const_(local_138);
      wcscpy_s((wchar_t *)(*(int *)(param_1 + 0x1c) + 100),0x32,pwVar5);
      puVar1 = *(undefined4 **)(*(int *)(param_1 + 0x398) + 0x558);
      uVar6 = (**(code **)(*(int *)(*(int *)(param_1 + 0x398) + 0x6c8) + 8))();
      piVar7 = (int *)(*(code *)*puVar1)(uVar6);
      if (piVar7 != (int *)0x0) {
        iVar2 = *piVar7;
        pwVar5 = DuiLib::CDuiString::operator_wchar_t_const_(local_138);
        (**(code **)(iVar2 + 0x2c))(pwVar5);
        DuiLib::CControlUI::Invalidate(*(CControlUI **)(param_1 + 0x398));
      }
      FUN_004116c0(param_1);
    }
    (**(code **)(*(int *)pCVar4 + 0xf8))(0);
    local_a30[0] = CEditMacroName::vftable;
    local_a20 = CEditMacroName::vftable;
    local_a10 = CEditMacroName::vftable;
    local_a0c = CEditMacroName::vftable;
    local_a08 = CEditMacroName::vftable;
    local_a04 = CEditMacroName::vftable;
    DuiLib::CDuiString::~CDuiString(local_138);
    DuiLib::CDuiString::~CDuiString(local_1bc);
    DuiLib::CDuiString::~CDuiString(local_244);
    DuiLib::CDuiString::~CDuiString(local_2c8);
    DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_a30);
    DuiLib::CDuiString::~CDuiString(local_98);
  }
  ExceptionList = local_10;
  return;
}


