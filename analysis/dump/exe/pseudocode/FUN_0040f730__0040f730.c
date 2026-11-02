// Program: SM809 mouse Software.exe
// Function: FUN_0040f730
// Entry: 0040f730
// Body: 0040f730 - 0040f9c5
// Signature: undefined FUN_0040f730(void * this, int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_0040f730(void *this,int param_1)

{
  CDuiString *this_00;
  wchar_t *pwVar1;
  void *pvVar2;
  int iVar3;
  int *piVar4;
  CDuiString in_stack_fffffdc0;
  CDuiString aCStack_23d [121];
  CDuiString local_1a8 [136];
  void *local_120;
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00422739;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  iVar3 = *(int *)(param_1 + 0x108);
  if (iVar3 == *(int *)((int)this + 0x338)) {
    iVar3 = *(int *)(param_1 + 0x118);
    *(int *)((int)this + 0x310) = iVar3;
    DuiLib::CDuiString::CDuiString(local_11c);
    local_8 = 0;
    this_00 = DuiLib::CStdPtrArray::operator[]((CStdPtrArray *)((int)this + 0x304),iVar3);
    pwVar1 = DuiLib::CDuiString::GetData(this_00);
    DuiLib::CDuiString::operator=(local_11c,pwVar1);
    DuiLib::CDuiString::CDuiString(local_1a8,local_11c);
    local_8._0_1_ = 1;
    DuiLib::CDuiString::CDuiString(local_98);
    local_8 = CONCAT31(local_8._1_3_,2);
    local_120 = (void *)0x0;
    (**(code **)(*(int *)(*(int *)((int)this + 0x398) + 0x558) + 0x20))();
    (**(code **)(*(int *)(*(int *)((int)this + 0x360) + 0x558) + 0x20))();
    DuiLib::CStdPtrArray::Empty((CStdPtrArray *)((int)this + 0x2f8));
    if (DAT_0046c380 != DAT_0046c384) {
      pvVar2 = (void *)0x0;
      piVar4 = DAT_0046c380;
      do {
        pwVar1 = (wchar_t *)*piVar4;
        if (*(int *)(pwVar1 + 0x6a) == 0) {
          iVar3 = DuiLib::CDuiString::CompareNoCase(local_1a8,pwVar1);
          if (iVar3 == 0) {
            DuiLib::CDuiString::operator=(local_98,pwVar1 + 0x32);
            DuiLib::CStdPtrArray::Add((CStdPtrArray *)((int)this + 0x2f8),local_120);
            DuiLib::CDuiString::CDuiString(aCStack_23d + -3,local_98);
            FUN_00413500((int)this,in_stack_fffffdc0);
          }
          pvVar2 = local_120;
        }
        pvVar2 = (void *)((int)pvVar2 + 1);
        piVar4 = piVar4 + 1;
        local_120 = pvVar2;
      } while (piVar4 != DAT_0046c384);
    }
    *(undefined4 *)((int)this + 0x314) = 0xffffffff;
    *(undefined4 *)((int)this + 0x2c0) = 0;
    memset((void *)((int)this + 0x24),0,0x280);
    *(undefined4 *)((int)this + 0x2a4) = 0;
    *(undefined4 *)((int)this + 700) = 0xffffffff;
    FUN_00411740(this,-1);
    (**(code **)(**(int **)((int)this + 0x348) + 0x2c))();
    (**(code **)(**(int **)((int)this + 0x388) + 0x2c))();
    *(undefined4 *)((int)this + 0x1c) = 0;
    FUN_00411220((int)this);
    DuiLib::CDuiString::~CDuiString(local_98);
    DuiLib::CDuiString::~CDuiString(local_1a8);
    DuiLib::CDuiString::~CDuiString(local_11c);
  }
  else if (iVar3 == *(int *)((int)this + 0x398)) {
    pvVar2 = DuiLib::CStdPtrArray::GetAt
                       ((CStdPtrArray *)((int)this + 0x2f8),*(int *)(param_1 + 0x118));
    *(void **)((int)this + 0x314) = pvVar2;
    FUN_00410990(this,(uint)pvVar2);
  }
  else if (iVar3 == *(int *)((int)this + 0x360)) {
    iVar3 = *(int *)(param_1 + 0x118);
    *(int *)((int)this + 700) = iVar3;
    FUN_00411740(this,iVar3);
  }
  else if ((iVar3 == *(int *)((int)this + 900)) && (-1 < *(int *)((int)this + 700))) {
    *(char *)((int)this + *(int *)((int)this + 700) * 0x10 + 0x25) =
         *(char *)(param_1 + 0x118) + -0x10;
    FUN_00411ae0(this,*(int *)((int)this + 700));
    FUN_004116c0((int)this);
  }
  ExceptionList = local_10;
  return;
}


