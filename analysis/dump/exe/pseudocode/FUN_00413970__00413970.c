// Program: SM809 mouse Software.exe
// Function: FUN_00413970
// Entry: 00413970
// Body: 00413970 - 00413c69
// Signature: undefined FUN_00413970(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_00413970(int param_1)

{
  CDuiString *pCVar1;
  wchar_t *pwVar2;
  CControlUI *pCVar3;
  uint uVar4;
  void *pvVar5;
  int iVar6;
  wchar_t *_Src;
  int *piVar7;
  undefined4 *puVar8;
  code *pcVar9;
  undefined **local_ab4 [4];
  undefined **local_aa4;
  undefined **local_a94;
  undefined **local_a90;
  undefined **local_a8c;
  undefined **local_a88;
  undefined4 **local_244;
  CDuiString local_1bc [132];
  undefined4 local_138;
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00422c5d;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  if (-1 < *(int *)(param_1 + 0x310)) {
    DuiLib::CDuiString::CDuiString(local_11c);
    local_8 = 0;
    DuiLib::CDuiString::CDuiString(local_98);
    local_8._0_1_ = 1;
    pCVar1 = DuiLib::CStdPtrArray::operator[]
                       ((CStdPtrArray *)(param_1 + 0x304),*(int *)(param_1 + 0x310));
    pwVar2 = DuiLib::CDuiString::GetData(pCVar1);
    DuiLib::CDuiString::operator=(local_11c,pwVar2);
    pCVar3 = DuiLib::CPaintManagerUI::FindControl
                       (*(CPaintManagerUI **)(param_1 + 0x10),L"disable_window_ver");
    (**(code **)(*(int *)pCVar3 + 0xf8))(1);
    memset(local_ab4,0,0x998);
    FUN_00409940((WindowImplBase *)local_ab4);
    local_8 = CONCAT31(local_8._1_3_,2);
    DuiLib::CDuiString::operator=(local_1bc,local_11c);
    local_138 = 2;
    local_244 = &DAT_0046c380;
    DuiLib::CWindowWnd::Create
              ((CWindowWnd *)local_ab4,*(HWND__ **)(param_1 + 0x14),L"EditMacroName",0x90000000,0x80
               ,0,0,800,800,(HMENU__ *)0x0);
    DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_ab4);
    uVar4 = DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_ab4);
    pcVar9 = ~CDuiString_exref;
    if (uVar4 == 1) {
      DuiLib::CDuiString::operator=(local_98,local_1bc);
      pCVar1 = DuiLib::CStdPtrArray::operator[]
                         ((CStdPtrArray *)(param_1 + 0x304),*(int *)(param_1 + 0x310));
      if (pCVar1 != (CDuiString *)0x0) {
        DuiLib::CDuiString::~CDuiString(pCVar1);
        FUN_0041feb7(pCVar1);
      }
      pCVar1 = operator_new(0x84);
      local_8._0_1_ = 3;
      pvVar5 = (void *)DuiLib::CDuiString::CDuiString(pCVar1,local_98);
      local_8 = CONCAT31(local_8._1_3_,2);
      DuiLib::CStdPtrArray::SetAt
                ((CStdPtrArray *)(param_1 + 0x304),*(int *)(param_1 + 0x310),pvVar5);
      puVar8 = DAT_0046c380;
      if (DAT_0046c380 != DAT_0046c384) {
        do {
          pwVar2 = (wchar_t *)*puVar8;
          iVar6 = DuiLib::CDuiString::CompareNoCase(local_11c,pwVar2);
          if (iVar6 == 0) {
            _Src = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
            wcscpy_s(pwVar2,0x32,_Src);
          }
          puVar8 = puVar8 + 1;
        } while (puVar8 != DAT_0046c384);
        pcVar9 = ~CDuiString_exref;
      }
      FUN_00402ef0();
      piVar7 = (int *)(*(code *)**(undefined4 **)(*(int *)(param_1 + 0x338) + 0x558))
                                (*(undefined4 *)(param_1 + 0x310));
      if (piVar7 != (int *)0x0) {
        iVar6 = *piVar7;
        pwVar2 = DuiLib::CDuiString::GetData(local_98);
        (**(code **)(iVar6 + 0x2c))(pwVar2);
        DuiLib::CControlUI::Invalidate(*(CControlUI **)(param_1 + 0x338));
      }
    }
    (**(code **)(*(int *)pCVar3 + 0xf8))(0);
    local_ab4[0] = CEditMacroName::vftable;
    local_aa4 = CEditMacroName::vftable;
    local_a94 = CEditMacroName::vftable;
    local_a90 = CEditMacroName::vftable;
    local_a8c = CEditMacroName::vftable;
    local_a88 = CEditMacroName::vftable;
    (*pcVar9)();
    (*pcVar9)();
    (*pcVar9)();
    (*pcVar9)();
    DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_ab4);
    (*pcVar9)();
    (*pcVar9)();
  }
  ExceptionList = local_10;
  return;
}


