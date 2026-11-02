// Program: SM809 mouse Software.exe
// Function: FUN_0041e260
// Entry: 0041e260
// Body: 0041e260 - 0041e48a
// Signature: undefined FUN_0041e260(void * this, CDuiString * param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_0041e260(void *this,CDuiString *param_1)

{
  wchar_t *pwVar1;
  bool bVar2;
  uint uVar3;
  int iVar4;
  CDuiString *this_00;
  wchar_t *pwVar5;
  void *pvVar6;
  int iVar7;
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_004216e1;
  local_10 = ExceptionList;
  uVar3 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  local_14 = uVar3;
  bVar2 = DuiLib::CDuiString::operator==(param_1,L"click");
  if (bVar2) {
    (**(code **)(*(int *)((int)this + -0x20) + 0x20))(param_1,uVar3);
    ExceptionList = local_10;
    return;
  }
  bVar2 = DuiLib::CDuiString::operator==(param_1,L"selectchanged");
  if (bVar2) {
    iVar7 = 0;
    iVar4 = 0x774;
    do {
      if (*(int *)(param_1 + 0x108) == *(int *)(iVar4 + -0x20 + (int)this)) {
        *(int *)((int)this + 0x768) = iVar7;
        ExceptionList = local_10;
        return;
      }
      iVar4 = iVar4 + 4;
      iVar7 = iVar7 + 1;
    } while (iVar4 < 0x780);
    ExceptionList = local_10;
    return;
  }
  bVar2 = DuiLib::CDuiString::operator==(param_1,L"itemselect");
  if (bVar2) {
    FUN_0041e680((void *)((int)this + -0x20),(int)param_1);
    ExceptionList = local_10;
    return;
  }
  bVar2 = DuiLib::CDuiString::operator==(param_1,L"timer");
  if (!bVar2) {
    ExceptionList = local_10;
    return;
  }
  if (*(CControlUI **)(param_1 + 0x108) != *(CControlUI **)((int)this + 0x750)) {
    ExceptionList = local_10;
    return;
  }
  DuiLib::CPaintManagerUI::KillTimer
            ((CPaintManagerUI *)((int)this + 0x10),*(CControlUI **)((int)this + 0x750),1000);
  uVar3 = *(uint *)((int)this + 0x78c);
  if (DAT_0046c398 == DAT_0046c39c) {
    ExceptionList = local_10;
    return;
  }
  if ((int)uVar3 < 0) {
    ExceptionList = local_10;
    return;
  }
  if ((uint)(DAT_0046c39c - DAT_0046c398 >> 2) <= uVar3) {
                    /* WARNING: Subroutine does not return */
    FUN_004050f0();
  }
  pwVar1 = *(wchar_t **)(DAT_0046c398 + uVar3 * 4);
  if (pwVar1 == (wchar_t *)0x0) {
    ExceptionList = local_10;
    return;
  }
  DuiLib::CDuiString::CDuiString(local_98);
  local_8 = 0;
  iVar7 = 0;
  iVar4 = DuiLib::CStdPtrArray::GetSize((CStdPtrArray *)((int)this + 0x77c));
  if (0 < iVar4) {
    do {
      this_00 = DuiLib::CStdPtrArray::operator[]((CStdPtrArray *)((int)this + 0x77c),iVar7);
      pwVar5 = DuiLib::CDuiString::GetData(this_00);
      DuiLib::CDuiString::operator=(local_98,pwVar5);
      iVar4 = DuiLib::CDuiString::CompareNoCase(local_98,pwVar1);
      if (iVar4 == 0) {
        (**(code **)(*(int *)(*(int *)((int)this + 0x764) + 0x6a0) + 0xc))(iVar7,0);
        iVar7 = 0;
        iVar4 = DuiLib::CStdPtrArray::GetSize((CStdPtrArray *)((int)this + 0x770));
        if (0 < iVar4) goto LAB_0041e420;
        break;
      }
      iVar7 = iVar7 + 1;
      iVar4 = DuiLib::CStdPtrArray::GetSize((CStdPtrArray *)((int)this + 0x77c));
    } while (iVar7 < iVar4);
  }
  goto LAB_0041e45c;
  while( true ) {
    iVar7 = iVar7 + 1;
    iVar4 = DuiLib::CStdPtrArray::GetSize((CStdPtrArray *)((int)this + 0x770));
    if (iVar4 <= iVar7) break;
LAB_0041e420:
    pvVar6 = DuiLib::CStdPtrArray::operator[]((CStdPtrArray *)((int)this + 0x770),iVar7);
    if (pvVar6 == *(void **)((int)this + 0x78c)) {
      (**(code **)(*(int *)(*(int *)((int)this + 0x750) + 0x6c8) + 0xc))(iVar7,0);
      break;
    }
  }
LAB_0041e45c:
  DuiLib::CDuiString::~CDuiString(local_98);
  ExceptionList = local_10;
  return;
}


