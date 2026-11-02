// Program: SM809 mouse Software.exe
// Function: FUN_00403f90
// Entry: 00403f90
// Body: 00403f90 - 004040d8
// Signature: undefined FUN_00403f90(CDuiString param_1)


void __cdecl FUN_00403f90(CDuiString param_1)

{
  wchar_t wVar1;
  int iVar2;
  CDuiString *pCVar3;
  wchar_t *pwVar4;
  int iVar5;
  int iVar6;
  code *pcVar7;
  CDuiString local_1a0 [132];
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  CEditUI *local_14;
  void *local_10;
  undefined1 *puStack_c;
  int local_8;
  
  pcVar7 = GetLength_exref;
  puStack_c = &LAB_004213f2;
  local_10 = ExceptionList;
  ExceptionList = &local_10;
  local_8 = 0;
  iVar6 = 0;
  iVar2 = DuiLib::CDuiString::GetLength(&param_1);
  if (0 < iVar2) {
    do {
      wVar1 = DuiLib::CDuiString::GetAt(&param_1,iVar6);
      if ((((ushort)wVar1 < 0x30) ||
          (wVar1 = DuiLib::CDuiString::GetAt(&param_1,iVar6), 0x39 < (ushort)wVar1)) &&
         (wVar1 = DuiLib::CDuiString::GetAt(&param_1,iVar6), wVar1 != L'-')) {
        (*pcVar7)();
        DuiLib::CDuiString::Right(&param_1,(int)local_1a0);
        local_8._0_1_ = 1;
        pCVar3 = (CDuiString *)DuiLib::CDuiString::Left(&param_1,(int)local_11c);
        local_8._0_1_ = 2;
        pCVar3 = (CDuiString *)DuiLib::CDuiString::operator+(pCVar3,local_98);
        local_8._0_1_ = 3;
        DuiLib::CDuiString::operator=(&param_1,pCVar3);
        DuiLib::CDuiString::~CDuiString(local_98);
        DuiLib::CDuiString::~CDuiString(local_11c);
        local_8 = (uint)local_8._1_3_ << 8;
        DuiLib::CDuiString::~CDuiString(local_1a0);
        iVar2 = *(int *)local_14;
        pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(&param_1);
        (**(code **)(iVar2 + 0x2c))(pwVar4);
        pcVar7 = GetLength_exref;
        iVar2 = DuiLib::CDuiString::GetLength(&param_1);
        iVar5 = DuiLib::CDuiString::GetLength(&param_1);
        DuiLib::CEditUI::SetSel(local_14,iVar5,iVar2);
      }
      iVar6 = iVar6 + 1;
      iVar2 = (*pcVar7)();
    } while (iVar6 < iVar2);
  }
  DuiLib::CDuiString::~CDuiString(&param_1);
  ExceptionList = local_10;
  return;
}


