// Program: SM809 mouse Software.exe
// Function: FUN_0040ba50
// Entry: 0040ba50
// Body: 0040ba50 - 0040bce7
// Signature: undefined FUN_0040ba50(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_0040ba50(int param_1)

{
  uint uVar1;
  CControlUI *pCVar2;
  wchar_t *pwVar3;
  wchar_t *_Dst;
  undefined4 uVar4;
  int *piVar5;
  int iVar6;
  undefined4 *puVar7;
  undefined4 *puVar8;
  undefined4 uVar9;
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
  puStack_c = &LAB_00421f1c;
  local_10 = ExceptionList;
  uVar1 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  if (-1 < *(int *)(param_1 + 0x1ac)) {
    local_14 = uVar1;
    DuiLib::CDuiString::CDuiString(local_98);
    local_8 = 0;
    DuiLib::CDuiString::operator=(local_98,(wchar_t *)(*(int *)(param_1 + 0x1c) + 100));
    pCVar2 = DuiLib::CPaintManagerUI::FindControl
                       (*(CPaintManagerUI **)(param_1 + 0x10),L"disable_window_ver");
    (**(code **)(*(int *)pCVar2 + 0xf8))(1,uVar1);
    memset(local_a30,0,0x998);
    FUN_00409140((WindowImplBase *)local_a30);
    local_8 = CONCAT31(local_8._1_3_,1);
    DuiLib::CDuiString::operator=(local_138,local_98);
    DuiLib::CDuiString::operator=(local_1bc,*(wchar_t **)(param_1 + 0x1c));
    local_b4 = 3;
    local_1c0 = &DAT_0046c398;
    DuiLib::CWindowWnd::Create
              ((CWindowWnd *)local_a30,*(HWND__ **)(param_1 + 0x14),L"EditGunName",0x90000000,0x80,0
               ,0,800,800,(HMENU__ *)0x0);
    DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_a30);
    uVar1 = DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_a30);
    if (uVar1 == 1) {
      pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_138);
      _Dst = (wchar_t *)(*(int *)(param_1 + 0x1c) + 100);
      wcscpy_s(_Dst,0x32,pwVar3);
      puVar7 = *(undefined4 **)(*(int *)(param_1 + 0x684) + 0x558);
      uVar4 = (**(code **)(*(int *)(*(int *)(param_1 + 0x684) + 0x6c8) + 8))();
      uVar9 = 0x40bbc0;
      piVar5 = (int *)(*(code *)*puVar7)(uVar4);
      if (piVar5 != (int *)0x0) {
        iVar6 = *piVar5;
        pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_138);
        uVar9 = 0x40bbda;
        (**(code **)(iVar6 + 0x2c))(pwVar3);
        DuiLib::CControlUI::Invalidate(*(CControlUI **)(param_1 + 0x684));
      }
      iVar6 = *(int *)(param_1 + 0x1c);
      if ((iVar6 != 0) && (*(int *)(iVar6 + 0xcc) == 0)) {
        *(undefined1 *)(iVar6 + 200) = *(undefined1 *)(param_1 + 0x20);
        puVar7 = (undefined4 *)(param_1 + 0x28);
        puVar8 = (undefined4 *)(*(int *)(param_1 + 0x1c) + 0xd8);
        for (iVar6 = 0x5a; iVar6 != 0; iVar6 = iVar6 + -1) {
          *puVar8 = *puVar7;
          puVar7 = puVar7 + 1;
          puVar8 = puVar8 + 1;
        }
        FUN_00403350();
        iVar6 = FUN_00404200(*(uint *)(param_1 + 0x1ac),DAT_00432aa8,_Dst,uVar9,0);
        if (iVar6 != 0) {
          SendMessageW(*(HWND *)(param_1 + 0x14),0x467,0,0);
        }
      }
    }
    (**(code **)(*(int *)pCVar2 + 0xf8))(0);
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
    DuiLib::CDuiString::~CDuiString(local_98);
  }
  ExceptionList = local_10;
  return;
}


