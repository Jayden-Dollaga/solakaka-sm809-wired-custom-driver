// Program: SM809 mouse Software.exe
// Function: FUN_004178e0
// Entry: 004178e0
// Body: 004178e0 - 00417d0b
// Signature: undefined FUN_004178e0(void * this, int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_004178e0(void *this,int param_1)

{
  int iVar1;
  CMenuWnd *this_00;
  bool bVar2;
  uint uVar3;
  int *piVar4;
  undefined4 uVar5;
  wchar_t *pwVar6;
  CControlUI *pCVar7;
  CResourceManager *this_01;
  CDuiString *pCVar8;
  LPCWSTR lpParameters;
  LPCWSTR lpDirectory;
  INT nShowCmd;
  CDuiString local_9cc [132];
  int local_948;
  int iStack_944;
  int iStack_940;
  int iStack_93c;
  CMenuWnd *local_938;
  undefined **local_934 [4];
  undefined **local_924;
  undefined **local_914;
  undefined **local_910;
  undefined **local_90c;
  undefined **local_908;
  CDuiString local_1b8 [132];
  CDuiString local_134 [132];
  CDuiString local_b0 [132];
  tagRECT local_2c;
  int local_1c;
  int local_18;
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00423479;
  local_10 = ExceptionList;
  uVar3 = DAT_00432008 ^ (uint)(local_b0 + 0xac);
  ExceptionList = &local_10;
  iVar1 = *(int *)(param_1 + 0x108);
  local_14 = uVar3;
  if (iVar1 == *(int *)((int)this + 0x16e0)) {
    DuiLib::CWindowWnd::SendMessageW(this,0x112,0xf020,0);
  }
  else if (iVar1 == *(int *)((int)this + 0x16dc)) {
    DuiLib::CWindowWnd::ShowWindow(this,false,true);
  }
  else if (iVar1 == *(int *)((int)this + 0x1700)) {
    FUN_00417ec0((int)this);
  }
  else if (iVar1 == *(int *)((int)this + 0x1704)) {
    FUN_004181e0(this,DAT_00432aa8);
  }
  else if (iVar1 == *(int *)((int)this + 0x1708)) {
    this_00 = *(CMenuWnd **)((int)this + 0x1720);
    if (this_00 != (CMenuWnd *)0x0) {
      DuiLib::CMenuWnd::~CMenuWnd(this_00);
      FUN_0041feb7(this_00);
      *(undefined4 *)((int)this + 0x1720) = 0;
    }
    GetWindowRect(*(HWND *)((int)this + 4),&local_2c);
    piVar4 = (int *)(**(code **)(**(int **)((int)this + 0x1708) + 0x50))();
    local_948 = *piVar4;
    iStack_944 = piVar4[1];
    iStack_940 = piVar4[2];
    iStack_93c = piVar4[3];
    local_938 = operator_new(0x770);
    local_8 = 0;
    uVar5 = DuiLib::CMenuWnd::CMenuWnd(local_938);
    local_8 = 0xffffffff;
    *(undefined4 *)((int)this + 0x1720) = uVar5;
    DuiLib::CDuiPoint::CDuiPoint((CDuiPoint *)&local_1c);
    local_1c = local_948 + local_2c.left;
    local_18 = iStack_93c + local_2c.top;
    DuiLib::CMenuWnd::Init
              (*(CMenuWnd **)((int)this + 0x1720),0,L"profilemenu.xml",local_1c,local_18,
               (int)this + 0x30,0,6);
  }
  else if (iVar1 == *(int *)((int)this + 0x1710)) {
    local_938 = (CMenuWnd *)
                DuiLib::CPaintManagerUI::FindControl
                          ((CPaintManagerUI *)((int)this + 0x30),L"disable_window_ver");
    (**(code **)(*(int *)local_938 + 0xf8))(1);
    memset(local_934,0,0x884);
    FUN_0041c1c0((WindowImplBase *)local_934);
    local_8 = 1;
    DuiLib::CDuiString::operator=(local_1b8,L"warning_title_text");
    DuiLib::CDuiString::operator=(local_134,L"reset_profile_text");
    DuiLib::CWindowWnd::Create
              ((CWindowWnd *)local_934,*(HWND__ **)((int)this + 4),L"MsgWnd",0x90000000,0x80,0,0,800
               ,800,(HMENU__ *)0x0);
    DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_934);
    uVar3 = DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_934);
    if (uVar3 == 1) {
      DuiLib::CDuiString::CDuiString(local_b0,DAT_00432aa0,-1);
      local_8._0_1_ = 2;
      memcpy(DAT_00432aa0,&DAT_00432ae0,0x1cc50);
      pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_b0);
      wcscpy_s(DAT_00432aa0,0x32,pwVar6);
      FUN_00417540((int)this);
      PostThreadMessageW(DAT_00432ab8,0x670,0,0);
      pCVar7 = DuiLib::CPaintManagerUI::FindControl
                         ((CPaintManagerUI *)((int)this + 0x30),L"ring_ver");
      (**(code **)(*(int *)pCVar7 + 0xf8))(1);
      local_8 = CONCAT31(local_8._1_3_,1);
      DuiLib::CDuiString::~CDuiString(local_b0);
    }
    (**(code **)(*(int *)local_938 + 0xf8))(0);
    local_934[0] = CMsgWnd::vftable;
    local_924 = CMsgWnd::vftable;
    local_914 = CMsgWnd::vftable;
    local_910 = CMsgWnd::vftable;
    local_90c = CMsgWnd::vftable;
    local_908 = CMsgWnd::vftable;
    DuiLib::CDuiString::~CDuiString(local_134);
    DuiLib::CDuiString::~CDuiString(local_1b8);
    DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_934);
  }
  else if (iVar1 == *(int *)((int)this + 0x1714)) {
    PostThreadMessageW(DAT_00432ab8,0x670,0,0);
    pCVar7 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)((int)this + 0x30),L"ring_ver")
    ;
    (**(code **)(*(int *)pCVar7 + 0xf8))(1,uVar3);
  }
  else if (iVar1 == *(int *)((int)this + 0x16e4)) {
    DuiLib::CDuiString::CDuiString(local_b0);
    pCVar8 = local_9cc;
    local_8 = 3;
    pwVar6 = L"website_text";
    this_01 = DuiLib::CResourceManager::GetInstance();
    pCVar8 = (CDuiString *)DuiLib::CResourceManager::GetText(this_01,(wchar_t *)pCVar8,pwVar6);
    local_8._0_1_ = 4;
    DuiLib::CDuiString::operator=(local_b0,pCVar8);
    local_8 = CONCAT31(local_8._1_3_,3);
    DuiLib::CDuiString::~CDuiString(local_9cc);
    bVar2 = DuiLib::CDuiString::IsEmpty(local_b0);
    if (!bVar2) {
      nShowCmd = 5;
      lpDirectory = L"";
      lpParameters = L"";
      pwVar6 = DuiLib::CDuiString::operator_wchar_t_const_(local_b0);
      ShellExecuteW(*(HWND *)((int)this + 4),L"open",pwVar6,lpParameters,lpDirectory,nShowCmd);
    }
    DuiLib::CDuiString::~CDuiString(local_b0);
  }
  ExceptionList = local_10;
  return;
}


