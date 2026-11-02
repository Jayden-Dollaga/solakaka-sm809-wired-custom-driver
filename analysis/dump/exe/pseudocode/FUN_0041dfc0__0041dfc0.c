// Program: SM809 mouse Software.exe
// Function: FUN_0041dfc0
// Entry: 0041dfc0
// Body: 0041dfc0 - 0041e258
// Signature: undefined FUN_0041dfc0(CDuiString * param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_0041dfc0(CDuiString *param_1)

{
  CPaintManagerUI *pCVar1;
  uint uVar2;
  CDuiString *pCVar3;
  CControlUI *pCVar4;
  wchar_t *pwVar5;
  void *pvVar6;
  CListLabelElementUI *this;
  int *piVar7;
  CDuiString *extraout_ECX;
  CDuiString *this_00;
  CDuiString *extraout_ECX_00;
  int iVar8;
  int *piVar9;
  CDuiString *pCVar10;
  code *pcVar11;
  CDuiString local_1a8 [132];
  CDuiString *local_124;
  CPaintManagerUI *local_120;
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00423a43;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  pCVar1 = (CPaintManagerUI *)(param_1 + 0x30);
  local_124 = param_1;
  local_120 = pCVar1;
  pCVar4 = DuiLib::CPaintManagerUI::FindControl(pCVar1,L"ok_btn");
  *(CControlUI **)(param_1 + 0x764) = pCVar4;
  pCVar4 = DuiLib::CPaintManagerUI::FindControl(pCVar1,L"cancel_btn");
  *(CControlUI **)(param_1 + 0x768) = pCVar4;
  pCVar4 = DuiLib::CPaintManagerUI::FindControl(pCVar1,L"exit_btn");
  *(CControlUI **)(param_1 + 0x76c) = pCVar4;
  pCVar4 = DuiLib::CPaintManagerUI::FindControl(pCVar1,L"gun_list");
  *(CControlUI **)(param_1 + 0x770) = pCVar4;
  pCVar4 = DuiLib::CPaintManagerUI::FindControl(pCVar1,L"btn_gun_color");
  *(CControlUI **)(param_1 + 0x780) = pCVar4;
  pCVar4 = DuiLib::CPaintManagerUI::FindControl(pCVar1,L"gun_combo");
  *(CControlUI **)(param_1 + 0x784) = pCVar4;
  DuiLib::CDuiString::CDuiString(local_11c);
  pCVar1 = local_120;
  local_8 = 0;
  pCVar10 = param_1 + 0x774;
  iVar8 = 0;
  this_00 = extraout_ECX;
  do {
    iVar8 = iVar8 + 1;
    DuiLib::CDuiString::Format(this_00,(wchar_t *)local_11c,L"repeat_%d",iVar8);
    pwVar5 = DuiLib::CDuiString::operator_wchar_t_const_(local_11c);
    pCVar4 = DuiLib::CPaintManagerUI::FindControl(pCVar1,pwVar5);
    pCVar3 = local_124;
    *(CControlUI **)pCVar10 = pCVar4;
    pCVar10 = pCVar10 + 4;
    this_00 = extraout_ECX_00;
  } while (iVar8 < 3);
  (**(code **)(**(int **)(local_124 + *(int *)(local_124 + 0x788) * 4 + 0x774) + 0x1bc))(1,1);
  DuiLib::CDuiString::CDuiString(local_98);
  local_8 = CONCAT31(local_8._1_3_,1);
  DuiLib::CStdPtrArray::Empty((CStdPtrArray *)(pCVar3 + 0x79c));
  piVar7 = DAT_0046c39c;
  piVar9 = DAT_0046c398;
  pcVar11 = ~CDuiString_exref;
  if (DAT_0046c398 != DAT_0046c39c) {
    do {
      pwVar5 = (wchar_t *)*piVar9;
      if (*(int *)(pwVar5 + 0x68) == 1) {
        DuiLib::CDuiString::operator=(local_98,pwVar5);
        local_124 = operator_new(0x84);
        local_8._0_1_ = 2;
        pvVar6 = (void *)DuiLib::CDuiString::CDuiString(local_124,local_98);
        local_8._0_1_ = 1;
        DuiLib::CStdPtrArray::Add((CStdPtrArray *)(pCVar3 + 0x79c),pvVar6);
        DuiLib::CDuiString::CDuiString(local_1a8,pwVar5,-1);
        local_8._0_1_ = 3;
        this = operator_new(0x570);
        local_8._0_1_ = 4;
        local_120 = (CPaintManagerUI *)this;
        DuiLib::CListLabelElementUI::CListLabelElementUI(this);
        *(undefined ***)this = DuiLib::CListLabelElementUI::vftable;
        local_8._0_1_ = 3;
        pwVar5 = DuiLib::CDuiString::operator_wchar_t_const_(local_1a8);
        DuiLib::CControlUI::SetText((CControlUI *)this,pwVar5);
        (**(code **)(*(int *)this + 0x88))(0x19);
        (**(code **)(*(int *)(*(int *)(pCVar3 + 0x784) + 0x558) + 0x10))(this);
        pcVar11 = ~CDuiString_exref;
        local_8 = CONCAT31(local_8._1_3_,1);
        DuiLib::CDuiString::~CDuiString(local_1a8);
        piVar7 = DAT_0046c39c;
      }
      else {
        pcVar11 = ~CDuiString_exref;
      }
      piVar9 = piVar9 + 1;
    } while (piVar9 != piVar7);
  }
  uVar2 = *(uint *)(pCVar3 + 0x78c);
  DuiLib::CControlUI::SetBkColor
            (*(CControlUI **)(pCVar3 + 0x780),
             uVar2 >> 0x10 & 0xff | (uVar2 | 0xffffff00) << 0x10 | uVar2 & 0xff00);
  (*pcVar11)();
  (*pcVar11)();
  ExceptionList = local_10;
  return;
}


