// Program: SM809 mouse Software.exe
// Function: FUN_00410390
// Entry: 00410390
// Body: 00410390 - 00410689
// Signature: undefined FUN_00410390(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_00410390(int param_1)

{
  int iVar1;
  CDuiString *this;
  wchar_t *pwVar2;
  CControlUI *pCVar3;
  uint uVar4;
  wchar_t *pwVar5;
  CDuiString in_stack_fffff4a4;
  CDuiString aCStack_b59 [97];
  wchar_t *local_ab8;
  undefined **local_ab4 [4];
  undefined **local_aa4;
  undefined **local_a94;
  undefined **local_a90;
  undefined **local_a8c;
  undefined **local_a88;
  CDuiString local_34c [132];
  CDuiString local_2c8 [132];
  int *local_244;
  CDuiString local_240 [132];
  CDuiString local_1bc [132];
  undefined4 local_138;
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00422828;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  if (-1 < *(int *)(param_1 + 0x310)) {
    DuiLib::CDuiString::CDuiString(local_98);
    local_8 = 0;
    this = DuiLib::CStdPtrArray::operator[]
                     ((CStdPtrArray *)(param_1 + 0x304),*(int *)(param_1 + 0x310));
    pwVar2 = DuiLib::CDuiString::GetData(this);
    DuiLib::CDuiString::operator=(local_98,pwVar2);
    pCVar3 = DuiLib::CPaintManagerUI::FindControl
                       (*(CPaintManagerUI **)(param_1 + 0x10),L"disable_window_ver");
    (**(code **)(*(int *)pCVar3 + 0xf8))();
    memset(local_ab4,0,0x998);
    FUN_00409940((WindowImplBase *)local_ab4);
    local_8._0_1_ = 1;
    local_138 = 1;
    DuiLib::CDuiString::operator=(local_240,local_98);
    local_244 = &DAT_0046c380;
    DuiLib::CWindowWnd::Create
              ((CWindowWnd *)local_ab4,*(HWND__ **)(param_1 + 0x14),L"EditMacroName",0x90000000,0x80
               ,0,0,800,800,(HMENU__ *)0x0);
    DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_ab4);
    uVar4 = DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_ab4);
    if (uVar4 == 1) {
      DuiLib::CDuiString::CDuiString(local_11c,local_1bc);
      local_8 = CONCAT31(local_8._1_3_,2);
      pwVar2 = operator_new(0x358);
      local_ab8 = pwVar2;
      memset(pwVar2,0,0x358);
      pwVar2[100] = L'\x01';
      pwVar5 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
      wcscpy_s(pwVar2,0x32,pwVar5);
      pwVar5 = DuiLib::CDuiString::operator_wchar_t_const_(local_11c);
      pwVar2 = local_ab8;
      wcscpy_s(local_ab8 + 0x32,0x32,pwVar5);
      if (DAT_0046c384 == DAT_0046c388) {
        FUN_00405690(DAT_0046c384,&local_ab8);
      }
      else {
        *DAT_0046c384 = pwVar2;
        DAT_0046c384 = DAT_0046c384 + 1;
      }
      FUN_00402ef0();
      DuiLib::CStdPtrArray::Add
                ((CStdPtrArray *)(param_1 + 0x2f8),
                 (void *)(((int)DAT_0046c384 - DAT_0046c380 >> 2) + -1));
      DuiLib::CDuiString::CDuiString(aCStack_b59 + -3,local_11c);
      FUN_00413500(param_1,in_stack_fffff4a4);
      iVar1 = *(int *)(*(int *)(param_1 + 0x398) + 0x6c8);
      (**(code **)(*(int *)(*(int *)(param_1 + 0x398) + 0x558) + 0xc))();
      (**(code **)(iVar1 + 0xc))();
      local_8._0_1_ = 1;
      DuiLib::CDuiString::~CDuiString(local_11c);
    }
    (**(code **)(*(int *)pCVar3 + 0xf8))();
    local_ab4[0] = CEditMacroName::vftable;
    local_aa4 = CEditMacroName::vftable;
    local_a94 = CEditMacroName::vftable;
    local_a90 = CEditMacroName::vftable;
    local_a8c = CEditMacroName::vftable;
    local_a88 = CEditMacroName::vftable;
    DuiLib::CDuiString::~CDuiString(local_1bc);
    DuiLib::CDuiString::~CDuiString(local_240);
    DuiLib::CDuiString::~CDuiString(local_2c8);
    DuiLib::CDuiString::~CDuiString(local_34c);
    DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_ab4);
    DuiLib::CDuiString::~CDuiString(local_98);
  }
  ExceptionList = local_10;
  return;
}


