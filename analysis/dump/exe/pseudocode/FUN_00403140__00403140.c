// Program: SM809 mouse Software.exe
// Function: FUN_00403140
// Entry: 00403140
// Body: 00403140 - 0040321f
// Signature: undefined4 FUN_00403140(int * param_1, CDuiString param_2)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

undefined4 __thiscall FUN_00403140(int *param_1,CDuiString param_2)

{
  uint uVar1;
  wchar_t *pwVar2;
  int iVar3;
  undefined4 uVar4;
  undefined4 *puVar5;
  code *pcVar6;
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  puStack_c = &LAB_00421116;
  local_10 = ExceptionList;
  uVar1 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  local_8 = 0;
  local_14 = uVar1;
  DuiLib::CDuiString::CDuiString(local_98);
  local_8._0_1_ = 1;
  uVar4 = 0;
  pcVar6 = ~CDuiString_exref;
  if (*param_1 != param_1[1]) {
    DuiLib::CDuiString::CDuiString(local_11c);
    local_8._0_1_ = 2;
    puVar5 = (undefined4 *)*param_1;
    if (puVar5 != (undefined4 *)param_1[1]) {
      do {
        DuiLib::CDuiString::operator=(local_98,(wchar_t *)*puVar5);
        pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(&param_2);
        iVar3 = DuiLib::CDuiString::CompareNoCase(local_98,pwVar2);
        if (iVar3 == 0) {
          uVar4 = 1;
          break;
        }
        puVar5 = puVar5 + 1;
      } while (puVar5 != (undefined4 *)param_1[1]);
    }
    pcVar6 = ~CDuiString_exref;
    DuiLib::CDuiString::~CDuiString(local_11c);
  }
  (*pcVar6)(uVar1);
  (*pcVar6)();
  ExceptionList = local_10;
  return uVar4;
}


