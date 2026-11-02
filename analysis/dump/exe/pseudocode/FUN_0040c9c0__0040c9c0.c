// Program: SM809 mouse Software.exe
// Function: FUN_0040c9c0
// Entry: 0040c9c0
// Body: 0040c9c0 - 0040ccd7
// Signature: undefined FUN_0040c9c0(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_0040c9c0(int param_1)

{
  int iVar1;
  uint uVar2;
  CControlUI *pCVar3;
  CDuiString *_Dst;
  wchar_t *pwVar4;
  void *pvVar5;
  CListLabelElementUI *this;
  int iVar6;
  CDuiString local_abc [132];
  CDuiString *local_a38;
  int local_a34;
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
  puStack_c = &LAB_00422142;
  local_10 = ExceptionList;
  uVar2 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  local_a34 = param_1;
  local_14 = uVar2;
  pCVar3 = DuiLib::CPaintManagerUI::FindControl
                     (*(CPaintManagerUI **)(param_1 + 0x10),L"disable_window_ver");
  (**(code **)(*(int *)pCVar3 + 0xf8))(1,uVar2);
  memset(local_a30,0,0x998);
  FUN_00409140((WindowImplBase *)local_a30);
  local_8 = 0;
  local_b4 = 0;
  local_1c0 = &DAT_0046c398;
  DuiLib::CWindowWnd::Create
            ((CWindowWnd *)local_a30,*(HWND__ **)(param_1 + 0x14),L"EditGunName",0x90000000,0x80,0,0
             ,800,800,(HMENU__ *)0x0);
  DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_a30);
  uVar2 = DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_a30);
  if (uVar2 == 1) {
    DuiLib::CDuiString::CDuiString(local_98,local_138);
    local_8 = CONCAT31(local_8._1_3_,1);
    _Dst = operator_new(0x240);
    local_a38 = _Dst;
    memset(_Dst,0,0xd0);
    memset(_Dst + 0xd4,0,0x16c);
    *(undefined4 *)(_Dst + 0xd0) = 1;
    pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    wcscpy_s((wchar_t *)_Dst,0x32,pwVar4);
    if (DAT_0046c39c == DAT_0046c3a0) {
      FUN_00405510(DAT_0046c39c,&local_a38);
    }
    else {
      *DAT_0046c39c = _Dst;
      DAT_0046c39c = DAT_0046c39c + 1;
    }
    local_a38 = operator_new(0x84);
    local_8._0_1_ = 2;
    pvVar5 = (void *)DuiLib::CDuiString::CDuiString(local_a38,local_98);
    local_8._0_1_ = 1;
    DuiLib::CStdPtrArray::Add((CStdPtrArray *)(local_a34 + 0x19c),pvVar5);
    FUN_00403350();
    DuiLib::CDuiString::CDuiString(local_abc,local_98);
    local_8._0_1_ = 3;
    this = operator_new(0x570);
    local_8._0_1_ = 4;
    local_a38 = (CDuiString *)this;
    DuiLib::CListLabelElementUI::CListLabelElementUI(this);
    *(undefined ***)this = DuiLib::CListLabelElementUI::vftable;
    local_8._0_1_ = 3;
    pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_abc);
    DuiLib::CControlUI::SetText((CControlUI *)this,pwVar4);
    (**(code **)(*(int *)this + 0x88))(0x19);
    (**(code **)(*(int *)(*(int *)(local_a34 + 0x1b0) + 0x558) + 0x10))(this);
    local_8._0_1_ = 1;
    DuiLib::CDuiString::~CDuiString(local_abc);
    iVar1 = *(int *)(*(int *)(local_a34 + 0x1b0) + 0x6a0);
    iVar6 = (**(code **)(*(int *)(*(int *)(local_a34 + 0x1b0) + 0x558) + 0xc))(0);
    (**(code **)(iVar1 + 0xc))(iVar6 + -1);
    local_8 = (uint)local_8._1_3_ << 8;
    DuiLib::CDuiString::~CDuiString(local_98);
  }
  (**(code **)(*(int *)pCVar3 + 0xf8))(0);
  local_a30[0] = CEditGunName::vftable;
  local_a20 = CEditGunName::vftable;
  local_a10 = CEditGunName::vftable;
  local_a0c = CEditGunName::vftable;
  local_a08 = CEditGunName::vftable;
  local_a04 = CEditGunName::vftable;
  DuiLib::CDuiString::~CDuiString(local_138);
  DuiLib::CDuiString::~CDuiString(local_1bc);
  DuiLib::CDuiString::~CDuiString(local_244);
  DuiLib::CDuiString::~CDuiString(local_2c8);
  DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_a30);
  ExceptionList = local_10;
  return;
}


