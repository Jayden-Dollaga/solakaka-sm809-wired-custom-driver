// Program: SM809 mouse Software.exe
// Function: FUN_0040b080
// Entry: 0040b080
// Body: 0040b080 - 0040b37c
// Signature: undefined FUN_0040b080(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_0040b080(int param_1)

{
  CDuiString *this;
  wchar_t *pwVar1;
  CControlUI *pCVar2;
  uint uVar3;
  wchar_t *pwVar4;
  int iVar5;
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
  puStack_c = &LAB_00421e48;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  if (-1 < *(int *)(param_1 + 0x1a8)) {
    DuiLib::CDuiString::CDuiString(local_11c);
    local_8 = 0;
    this = DuiLib::CStdPtrArray::operator[]
                     ((CStdPtrArray *)(param_1 + 0x19c),*(int *)(param_1 + 0x1a8));
    pwVar1 = DuiLib::CDuiString::GetData(this);
    DuiLib::CDuiString::operator=(local_11c,pwVar1);
    pCVar2 = DuiLib::CPaintManagerUI::FindControl
                       (*(CPaintManagerUI **)(param_1 + 0x10),L"disable_window_ver");
    (**(code **)(*(int *)pCVar2 + 0xf8))();
    memset(local_ab4,0,0x998);
    FUN_00409140((WindowImplBase *)local_ab4);
    local_8._0_1_ = 1;
    local_138 = 1;
    local_244 = &DAT_0046c398;
    DuiLib::CWindowWnd::Create
              ((CWindowWnd *)local_ab4,*(HWND__ **)(param_1 + 0x14),L"EditGunName",0x90000000,0x80,0
               ,0,800,800,(HMENU__ *)0x0);
    DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_ab4);
    uVar3 = DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_ab4);
    if (uVar3 == 1) {
      DuiLib::CDuiString::CDuiString(local_98,local_1bc);
      local_8 = CONCAT31(local_8._1_3_,2);
      pwVar1 = operator_new(0x240);
      local_ab8 = pwVar1;
      memset(pwVar1,0,0x240);
      *(undefined1 *)(pwVar1 + 100) = 0x1e;
      pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_11c);
      wcscpy_s(pwVar1,0x32,pwVar4);
      pwVar1 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
      pwVar4 = local_ab8;
      wcscpy_s(local_ab8 + 0x32,0x32,pwVar1);
      pwVar1 = pwVar4 + 0x71;
      iVar5 = 0x1e;
      do {
        *pwVar1 = L'\n';
        pwVar1 = pwVar1 + 6;
        iVar5 = iVar5 + -1;
      } while (iVar5 != 0);
      if (DAT_0046c39c == DAT_0046c3a0) {
        FUN_00405510(DAT_0046c39c,&local_ab8);
      }
      else {
        *DAT_0046c39c = pwVar4;
        DAT_0046c39c = DAT_0046c39c + 1;
      }
      FUN_00403350();
      DuiLib::CStdPtrArray::Add
                ((CStdPtrArray *)(param_1 + 400),
                 (void *)(((int)DAT_0046c39c - DAT_0046c398 >> 2) + -1));
      DuiLib::CDuiString::CDuiString(aCStack_b59 + -3,local_98);
      FUN_0040cce0(param_1,in_stack_fffff4a4);
      iVar5 = *(int *)(*(int *)(param_1 + 0x684) + 0x6c8);
      (**(code **)(*(int *)(*(int *)(param_1 + 0x684) + 0x558) + 0xc))();
      (**(code **)(iVar5 + 0xc))();
      local_8._0_1_ = 1;
      DuiLib::CDuiString::~CDuiString(local_98);
    }
    (**(code **)(*(int *)pCVar2 + 0xf8))();
    local_ab4[0] = CEditGunName::vftable;
    local_aa4 = CEditGunName::vftable;
    local_a94 = CEditGunName::vftable;
    local_a90 = CEditGunName::vftable;
    local_a8c = CEditGunName::vftable;
    local_a88 = CEditGunName::vftable;
    DuiLib::CDuiString::~CDuiString(local_1bc);
    DuiLib::CDuiString::~CDuiString(local_240);
    DuiLib::CDuiString::~CDuiString(local_2c8);
    DuiLib::CDuiString::~CDuiString(local_34c);
    DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_ab4);
    DuiLib::CDuiString::~CDuiString(local_11c);
  }
  ExceptionList = local_10;
  return;
}


