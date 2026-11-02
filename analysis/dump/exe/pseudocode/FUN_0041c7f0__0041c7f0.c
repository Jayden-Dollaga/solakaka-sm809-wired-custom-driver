// Program: SM809 mouse Software.exe
// Function: FUN_0041c7f0
// Entry: 0041c7f0
// Body: 0041c7f0 - 0041cac7
// Signature: undefined FUN_0041c7f0(void * param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_0041c7f0(void *param_1)

{
  int iVar1;
  uint uVar2;
  void *pvVar3;
  CDuiString *this;
  wchar_t *pwVar4;
  CDuiString *this_00;
  int *piVar5;
  code *pcVar6;
  CDuiString local_12c [132];
  void *local_a8;
  int local_a4;
  int local_a0;
  int local_9c;
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_004238ad;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  local_a8 = param_1;
  (**(code **)(*(int *)(*(int *)((int)param_1 + 0x134) + 0x6a0) + 0xc))
            (*(byte *)(DAT_00432aa0 + 0x139) - 1,0,local_14);
  FUN_0041d620(param_1,(uint)*(byte *)(DAT_00432aa0 + 0x139));
  (**(code **)(**(int **)((int)param_1 + *(int *)(DAT_00432aa0 + 0x80) * 4 + 0x18) + 0x1bc))(1,1);
  (**(code **)(**(int **)((int)param_1 + *(int *)(DAT_00432aa0 + 0x84) * 4 + 0x28) + 0x1bc))(1,1);
  local_9c = 8;
  local_a0 = 0x88 - (int)param_1;
  piVar5 = (int *)((int)param_1 + 0x48);
  local_a4 = -0x48 - (int)param_1;
  pcVar6 = SetValue_exref;
  do {
    if (piVar5[8] != 0) {
      (*pcVar6)(*(undefined4 *)((int)piVar5 + DAT_00432aa0 + (0x40 - (int)param_1)));
    }
    if (*piVar5 != 0) {
      this = FUN_00403d70(local_12c,*(int *)((int)piVar5 + DAT_00432aa0 + (0x40 - (int)param_1)));
      local_8 = 0;
      iVar1 = *(int *)*piVar5;
      pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(this);
      (**(code **)(iVar1 + 0x2c))(pwVar4);
      local_8 = 0xffffffff;
      DuiLib::CDuiString::~CDuiString(local_12c);
      pcVar6 = SetValue_exref;
    }
    uVar2 = *(uint *)((int)piVar5 + DAT_00432aa0 + local_a0);
    DuiLib::CControlUI::SetBkColor
              ((CControlUI *)piVar5[0x28],
               (uint)*(byte *)((int)piVar5 + DAT_00432aa0 + local_a4 + 0xd2) |
               (uVar2 | 0xffffff00) << 0x10 | uVar2 & 0xff00);
    pvVar3 = local_a8;
    piVar5 = piVar5 + 1;
    local_9c = local_9c + -1;
  } while (local_9c != 0);
  (*pcVar6)(*(undefined4 *)(DAT_00432aa0 + 100));
  (*pcVar6)(*(undefined4 *)(DAT_00432aa0 + 0x68));
  (*pcVar6)(*(undefined4 *)(DAT_00432aa0 + 0x6c));
  DuiLib::CCheckBoxUI::SetCheck
            (*(CCheckBoxUI **)((int)pvVar3 + 0x114),*(int *)(DAT_00432aa0 + 0x70) != 0);
  DuiLib::CCheckBoxUI::SetCheck
            (*(CCheckBoxUI **)((int)pvVar3 + 0x118),*(int *)(DAT_00432aa0 + 0x74) != 0);
  (*pcVar6)(*(undefined4 *)(DAT_00432aa0 + 0x130));
  DuiLib::CCheckBoxUI::SetCheck
            (*(CCheckBoxUI **)((int)pvVar3 + 0x124),*(int *)(DAT_00432aa0 + 0x134) != 0);
  (**(code **)(**(int **)((int)pvVar3 + 0x128) + 0xf8))(*(int *)(DAT_00432aa0 + 0x134) != 0);
  DuiLib::CDuiString::CDuiString(local_98);
  local_8 = 1;
  (*pcVar6)(*(undefined1 *)(DAT_00432aa0 + 0x138));
  DuiLib::CDuiString::Format
            (this_00,(wchar_t *)local_98,L"%d ms",(uint)*(byte *)(DAT_00432aa0 + 0x138));
  iVar1 = **(int **)((int)pvVar3 + 0x130);
  pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
  (**(code **)(iVar1 + 0x2c))(pwVar4);
  DuiLib::CDuiString::~CDuiString(local_98);
  ExceptionList = local_10;
  return;
}


