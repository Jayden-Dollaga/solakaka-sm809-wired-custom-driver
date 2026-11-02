// Program: SM809 mouse Software.exe
// Function: FUN_0041e680
// Entry: 0041e680
// Body: 0041e680 - 0041e8fe
// Signature: undefined FUN_0041e680(void * this, int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_0041e680(void *this,int param_1)

{
  void *pvVar1;
  CDuiString *this_00;
  wchar_t *pwVar2;
  int iVar3;
  CListLabelElementUI *this_01;
  int *piVar4;
  code *pcVar5;
  CDuiString local_234 [132];
  CDuiString local_1b0 [132];
  CListLabelElementUI *local_12c;
  CStdPtrArray *local_128;
  void *local_124;
  void *local_120;
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00423afa;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  local_124 = this;
  if (*(int *)(param_1 + 0x108) == *(int *)((int)this + 0x770)) {
    pvVar1 = DuiLib::CStdPtrArray::GetAt
                       ((CStdPtrArray *)((int)this + 0x790),*(int *)(param_1 + 0x118));
    *(void **)((int)this + 0x7ac) = pvVar1;
  }
  else if (*(int *)(param_1 + 0x108) == *(int *)((int)this + 0x784)) {
    iVar3 = *(int *)(param_1 + 0x118);
    *(int *)((int)this + 0x7a8) = iVar3;
    DuiLib::CDuiString::CDuiString(local_11c);
    local_8 = 0;
    this_00 = DuiLib::CStdPtrArray::operator[]((CStdPtrArray *)((int)this + 0x79c),iVar3);
    pwVar2 = DuiLib::CDuiString::GetData(this_00);
    DuiLib::CDuiString::operator=(local_11c,pwVar2);
    DuiLib::CDuiString::CDuiString(local_234,local_11c);
    local_8._0_1_ = 1;
    DuiLib::CDuiString::CDuiString(local_98);
    local_8 = CONCAT31(local_8._1_3_,2);
    local_120 = (void *)0x0;
    (**(code **)(*(int *)(*(int *)((int)this + 0x770) + 0x558) + 0x20))();
    local_128 = (CStdPtrArray *)((int)this + 0x790);
    DuiLib::CStdPtrArray::Empty(local_128);
    pcVar5 = ~CDuiString_exref;
    if (DAT_0046c398 != DAT_0046c39c) {
      pvVar1 = (void *)0x0;
      piVar4 = DAT_0046c398;
      do {
        pwVar2 = (wchar_t *)*piVar4;
        if (*(int *)(pwVar2 + 0x68) == 0) {
          iVar3 = DuiLib::CDuiString::CompareNoCase(local_234,pwVar2);
          if (iVar3 != 0) {
            pvVar1 = local_120;
            goto LAB_0041e89d;
          }
          DuiLib::CDuiString::operator=(local_98,pwVar2 + 0x32);
          DuiLib::CStdPtrArray::Add(local_128,local_120);
          iVar3 = *(int *)(pwVar2 + 0x66);
          DuiLib::CDuiString::CDuiString(local_1b0,local_98);
          local_8._0_1_ = 3;
          this_01 = operator_new(0x570);
          local_8._0_1_ = 4;
          local_12c = this_01;
          DuiLib::CListLabelElementUI::CListLabelElementUI(this_01);
          *(undefined ***)this_01 = DuiLib::CListLabelElementUI::vftable;
          local_8 = CONCAT31(local_8._1_3_,3);
          pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(local_1b0);
          DuiLib::CControlUI::SetText((CControlUI *)this_01,pwVar2);
          (**(code **)(*(int *)this_01 + 0x88))(0x1e);
          if (iVar3 != 0) {
            DuiLib::CControlUI::SetBkImage
                      ((CControlUI *)this_01,L"res=\'skins/lock.png\' dest=\'160,0,190,30\'");
          }
          (**(code **)(*(int *)(*(int *)((int)local_124 + 0x770) + 0x558) + 0x10))(this_01);
          pcVar5 = ~CDuiString_exref;
          local_8 = CONCAT31(local_8._1_3_,2);
          DuiLib::CDuiString::~CDuiString(local_1b0);
        }
        else {
LAB_0041e89d:
          local_120 = pvVar1;
          pcVar5 = ~CDuiString_exref;
        }
        pvVar1 = (void *)((int)local_120 + 1);
        piVar4 = piVar4 + 1;
        local_120 = pvVar1;
      } while (piVar4 != DAT_0046c39c);
      this = local_124;
    }
    *(undefined4 *)((int)this + 0x7ac) = 0xffffffff;
    (*pcVar5)();
    (*pcVar5)();
    (*pcVar5)();
  }
  ExceptionList = local_10;
  return;
}


