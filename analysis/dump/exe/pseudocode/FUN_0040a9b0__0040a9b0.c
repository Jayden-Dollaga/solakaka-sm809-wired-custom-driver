// Program: SM809 mouse Software.exe
// Function: FUN_0040a9b0
// Entry: 0040a9b0
// Body: 0040a9b0 - 0040ac00
// Signature: undefined FUN_0040a9b0(void * this, int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_0040a9b0(void *this,int param_1)

{
  CDuiString *this_00;
  wchar_t *pwVar1;
  void *pvVar2;
  int iVar3;
  int *piVar4;
  undefined4 *puVar5;
  undefined4 *puVar6;
  CDuiString in_stack_fffffdc0;
  CDuiString aCStack_23d [117];
  undefined4 in_stack_fffffe3c;
  undefined4 uVar7;
  CDuiString local_1a8 [136];
  void *local_120;
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00421d39;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  iVar3 = *(int *)(param_1 + 0x108);
  if (iVar3 == *(int *)((int)this + 0x1b0)) {
    iVar3 = *(int *)(param_1 + 0x118);
    *(int *)((int)this + 0x1a8) = iVar3;
    DuiLib::CDuiString::CDuiString(local_11c);
    local_8 = 0;
    this_00 = DuiLib::CStdPtrArray::operator[]((CStdPtrArray *)((int)this + 0x19c),iVar3);
    pwVar1 = DuiLib::CDuiString::GetData(this_00);
    DuiLib::CDuiString::operator=(local_11c,pwVar1);
    DuiLib::CDuiString::CDuiString(local_1a8,local_11c);
    local_8._0_1_ = 1;
    DuiLib::CDuiString::CDuiString(local_98);
    local_8 = CONCAT31(local_8._1_3_,2);
    local_120 = (void *)0x0;
    (**(code **)(*(int *)(*(int *)((int)this + 0x684) + 0x558) + 0x20))();
    DuiLib::CStdPtrArray::Empty((CStdPtrArray *)((int)this + 400));
    if (DAT_0046c398 != DAT_0046c39c) {
      pvVar2 = (void *)0x0;
      piVar4 = DAT_0046c398;
      do {
        pwVar1 = (wchar_t *)*piVar4;
        if (*(int *)(pwVar1 + 0x68) == 0) {
          iVar3 = DuiLib::CDuiString::CompareNoCase(local_1a8,pwVar1);
          if (iVar3 == 0) {
            DuiLib::CDuiString::operator=(local_98,pwVar1 + 0x32);
            DuiLib::CStdPtrArray::Add((CStdPtrArray *)((int)this + 400),local_120);
            DuiLib::CDuiString::CDuiString(aCStack_23d + -3,local_98);
            FUN_0040cce0((int)this,in_stack_fffffdc0);
          }
          pvVar2 = local_120;
        }
        pvVar2 = (void *)((int)pvVar2 + 1);
        piVar4 = piVar4 + 1;
        local_120 = pvVar2;
      } while (piVar4 != DAT_0046c39c);
    }
    *(undefined4 *)((int)this + 0x1ac) = 0xffffffff;
    FUN_0040b650(this,0xffffffff);
    DuiLib::CDuiString::~CDuiString(local_98);
    DuiLib::CDuiString::~CDuiString(local_1a8);
    DuiLib::CDuiString::~CDuiString(local_11c);
  }
  else if (iVar3 == *(int *)((int)this + 0x684)) {
    pvVar2 = DuiLib::CStdPtrArray::GetAt
                       ((CStdPtrArray *)((int)this + 400),*(int *)(param_1 + 0x118));
    *(void **)((int)this + 0x1ac) = pvVar2;
    FUN_0040b650(this,(uint)pvVar2);
  }
  else if (iVar3 == *(int *)((int)this + 0x1c4)) {
    iVar3 = *(int *)(param_1 + 0x118) + 1;
    *(int *)((int)this + 0x20) = iVar3;
    uVar7 = 0x40ab83;
    FUN_0040b9e0(this,iVar3);
    iVar3 = *(int *)((int)this + 0x1c);
    if ((iVar3 != 0) && (*(int *)(iVar3 + 0xcc) == 0)) {
      *(undefined1 *)(iVar3 + 200) = *(undefined1 *)((int)this + 0x20);
      puVar5 = (undefined4 *)((int)this + 0x28);
      puVar6 = (undefined4 *)(*(int *)((int)this + 0x1c) + 0xd8);
      for (iVar3 = 0x5a; iVar3 != 0; iVar3 = iVar3 + -1) {
        *puVar6 = *puVar5;
        puVar5 = puVar5 + 1;
        puVar6 = puVar6 + 1;
      }
      FUN_00403350();
      iVar3 = FUN_00404200(*(uint *)((int)this + 0x1ac),DAT_00432aa8,in_stack_fffffe3c,uVar7,0);
      if (iVar3 != 0) {
        SendMessageW(*(HWND *)((int)this + 0x14),0x467,0,0);
      }
    }
  }
  ExceptionList = local_10;
  return;
}


