// Program: SM809 mouse Software.exe
// Function: FUN_004039e0
// Entry: 004039e0
// Body: 004039e0 - 00403aec
// Signature: undefined4 FUN_004039e0(CDuiString param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

undefined4 __cdecl FUN_004039e0(CDuiString param_1)

{
  wchar_t *pwVar1;
  int iVar2;
  undefined4 uVar3;
  undefined4 *puVar4;
  CDuiString local_224 [132];
  CDuiString local_1a0 [132];
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  puStack_c = &LAB_004212de;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  local_8 = 0;
  DuiLib::CDuiString::CDuiString(local_224);
  local_8._0_1_ = 1;
  DuiLib::CDuiString::CDuiString(local_1a0);
  local_8._0_1_ = 2;
  DuiLib::CDuiString::CDuiString(local_11c);
  local_8._0_1_ = 3;
  uVar3 = 0;
  if (DAT_0046c38c != DAT_0046c390) {
    DuiLib::CDuiString::CDuiString(local_98);
    local_8._0_1_ = 4;
    puVar4 = DAT_0046c38c;
    if (DAT_0046c38c != DAT_0046c390) {
      do {
        DuiLib::CDuiString::operator=(local_98,(wchar_t *)*puVar4);
        pwVar1 = DuiLib::CDuiString::operator_wchar_t_const_(&param_1);
        iVar2 = DuiLib::CDuiString::CompareNoCase(local_98,pwVar1);
        if (iVar2 == 0) {
          uVar3 = 1;
          break;
        }
        puVar4 = puVar4 + 1;
      } while (puVar4 != DAT_0046c390);
    }
    DuiLib::CDuiString::~CDuiString(local_98);
  }
  DuiLib::CDuiString::~CDuiString(local_11c);
  DuiLib::CDuiString::~CDuiString(local_1a0);
  DuiLib::CDuiString::~CDuiString(local_224);
  DuiLib::CDuiString::~CDuiString(&param_1);
  ExceptionList = local_10;
  return uVar3;
}


