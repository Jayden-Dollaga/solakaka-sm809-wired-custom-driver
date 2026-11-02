// Program: SM809 mouse Software.exe
// Function: FUN_00403220
// Entry: 00403220
// Body: 00403220 - 0040334d
// Signature: undefined4 FUN_00403220(int * param_1, CDuiString param_2)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

undefined4 __thiscall FUN_00403220(int *param_1,CDuiString param_2)

{
  uint uVar1;
  wchar_t *pwVar2;
  int iVar3;
  undefined4 uVar4;
  undefined4 *puVar5;
  code *pcVar6;
  CDuiString CStack00000088;
  CDuiString local_1a0 [132];
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  puStack_c = &LAB_0042117e;
  local_10 = ExceptionList;
  uVar1 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  local_8 = 1;
  local_14 = uVar1;
  DuiLib::CDuiString::CDuiString(local_11c);
  local_8._0_1_ = 2;
  DuiLib::CDuiString::CDuiString(local_1a0);
  local_8._0_1_ = 3;
  if (*param_1 == param_1[1]) {
    uVar4 = 0;
    pcVar6 = ~CDuiString_exref;
  }
  else {
    DuiLib::CDuiString::CDuiString(local_98);
    local_8._0_1_ = 4;
    puVar5 = (undefined4 *)*param_1;
    if (puVar5 != (undefined4 *)param_1[1]) {
      do {
        pwVar2 = (wchar_t *)*puVar5;
        DuiLib::CDuiString::operator=(local_11c,pwVar2);
        DuiLib::CDuiString::operator=(local_98,pwVar2 + 0x32);
        pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(&CStack00000088);
        iVar3 = DuiLib::CDuiString::CompareNoCase(local_98,pwVar2);
        if (iVar3 == 0) {
          pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(&param_2);
          iVar3 = DuiLib::CDuiString::CompareNoCase(local_11c,pwVar2);
          if (iVar3 == 0) {
            uVar4 = 1;
            goto LAB_004032fe;
          }
        }
        puVar5 = puVar5 + 1;
      } while (puVar5 != (undefined4 *)param_1[1]);
    }
    uVar4 = 0;
LAB_004032fe:
    pcVar6 = ~CDuiString_exref;
    DuiLib::CDuiString::~CDuiString(local_98);
  }
  (*pcVar6)(uVar1);
  (*pcVar6)();
  (*pcVar6)();
  (*pcVar6)();
  ExceptionList = local_10;
  return uVar4;
}


