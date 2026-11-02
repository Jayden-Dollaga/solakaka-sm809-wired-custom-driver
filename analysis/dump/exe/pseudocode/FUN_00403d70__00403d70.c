// Program: SM809 mouse Software.exe
// Function: FUN_00403d70
// Entry: 00403d70
// Body: 00403d70 - 00403f5e
// Signature: CDuiString * FUN_00403d70(CDuiString * param_1, int param_2)


CDuiString * __fastcall FUN_00403d70(CDuiString *param_1,int param_2)

{
  uint uVar1;
  int iVar2;
  CDuiString *this;
  wchar_t *pwVar3;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  iVar2 = DAT_00432ad8;
  puStack_c = &LAB_0042139f;
  local_10 = ExceptionList;
  uVar1 = DAT_00432008 ^ (int)register0x00000010 - 4U;
  ExceptionList = &local_10;
  local_8 = 0;
  DuiLib::CDuiString::CDuiString(param_1);
  local_8 = 0;
  if ((((((iVar2 == 0xcfd) || (iVar2 == 0xcff)) || (iVar2 == 0xd07)) ||
       ((iVar2 == 0x24 || (iVar2 == 0x25)))) ||
      ((iVar2 == 0x26 || ((iVar2 == 0x3c || (iVar2 == 0xd05)))))) || (iVar2 == 0xcef)) {
    DuiLib::CDuiString::Format(this,(wchar_t *)param_1,&DAT_00424f54,param_2 * 100,uVar1);
    if (iVar2 != 0xd07) {
      ExceptionList = local_10;
      return param_1;
    }
    if (param_2 != 0xa0) {
      ExceptionList = local_10;
      return param_1;
    }
    pwVar3 = L"19000";
LAB_00403f43:
    DuiLib::CDuiString::operator=(param_1,pwVar3);
    ExceptionList = local_10;
    return param_1;
  }
  if ((iVar2 == 0xc8c) || (iVar2 == 0xc20)) {
    iVar2 = param_2 * 0x28;
  }
  else {
    if ((iVar2 != 0x1900) && (iVar2 != 0xd02)) {
      if (iVar2 != 0xd2a) {
        if (iVar2 != 0xbea) {
          ExceptionList = local_10;
          return param_1;
        }
        switch(param_2) {
        case 1:
          pwVar3 = L"250";
          break;
        case 2:
          pwVar3 = L"500";
          break;
        case 3:
          pwVar3 = L"750";
          break;
        default:
          pwVar3 = L"1000";
          break;
        case 5:
          pwVar3 = L"1250";
          break;
        case 6:
          pwVar3 = L"1500";
          break;
        case 7:
          pwVar3 = L"1750";
          break;
        case 8:
          pwVar3 = L"2000";
          break;
        case 9:
          pwVar3 = L"2500";
          break;
        case 10:
          pwVar3 = L"3000";
          break;
        case 0xb:
          pwVar3 = L"3500";
          break;
        case 0xc:
          pwVar3 = L"4000";
        }
        goto LAB_00403f43;
      }
      if (200 < param_2) {
        iVar2 = (param_2 + -100) * 100;
        goto LAB_00403e71;
      }
    }
    iVar2 = param_2 * 0x32;
  }
LAB_00403e71:
  DuiLib::CDuiString::Format(this,(wchar_t *)param_1,&DAT_00424f54,iVar2,uVar1);
  ExceptionList = local_10;
  return param_1;
}


