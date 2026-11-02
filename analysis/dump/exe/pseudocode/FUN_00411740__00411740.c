// Program: SM809 mouse Software.exe
// Function: FUN_00411740
// Entry: 00411740
// Body: 00411740 - 00411ad2
// Signature: undefined FUN_00411740(void * this, int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_00411740(void *this,int param_1)

{
  wchar_t *pwVar1;
  CResourceManager *this_00;
  CDuiString *this_01;
  CDuiString *this_02;
  CDuiString *this_03;
  int iVar2;
  CDuiString *pCVar3;
  code *pcVar4;
  CDuiString local_130 [132];
  undefined4 local_ac;
  undefined4 local_a8;
  CDuiString *local_a4;
  void *local_a0;
  CDuiString local_99;
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_004229e9;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  local_a0 = this;
  if (param_1 < 0) {
    (**(code **)(**(int **)((int)this + 0x374) + 0x2c))(&DAT_0042628c,local_14);
    (**(code **)(**(int **)((int)this + 0x378) + 0x2c))(&DAT_0042628c);
    (**(code **)(**(int **)((int)this + 0x37c) + 0xf8))(0);
    (**(code **)(**(int **)((int)this + 0x380) + 0xf8))(0);
    (**(code **)(**(int **)((int)this + 0x3a0) + 0xf8))(0);
    (**(code **)(*(int *)(*(int *)((int)this + 900) + 0x6a0) + 0xc))(0,0);
  }
  else {
    DuiLib::CDuiString::CDuiString(local_98);
    local_8 = 0;
    (**(code **)(**(int **)((int)this + 0x380) + 0xf8))(1);
    pCVar3 = (CDuiString *)(param_1 * 0x10 + (int)this);
    local_a8 = *(undefined4 *)(pCVar3 + 0x2c);
    local_99 = pCVar3[0x25];
    local_ac = *(undefined4 *)((int)this + (param_1 + 3) * 0x10);
    iVar2 = **(int **)((int)this + 0x37c);
    local_a4 = pCVar3;
    if ((byte)((char)local_99 + 0x10U) < 5) {
      (**(code **)(iVar2 + 0xf8))(1);
      (**(code **)(**(int **)((int)this + 0x3a0) + 0xf8))(0);
      (**(code **)(**(int **)((int)this + 0x374) + 0xf8))(0);
      (**(code **)(**(int **)((int)this + 900) + 0xf8))(1);
      (**(code **)(*(int *)(*(int *)((int)this + 900) + 0x6a0) + 0xc))((byte)local_99 - 0xf0,0);
      DuiLib::CDuiString::Format
                (this_01,(wchar_t *)local_98,&DAT_00424f54,(uint)*(ushort *)(pCVar3 + 0x28));
      iVar2 = **(int **)((int)this + 0x378);
      pwVar1 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
    }
    else {
      if (local_99 == (CDuiString)0xf6) {
        (**(code **)(iVar2 + 0xf8))(0);
        (**(code **)(**(int **)((int)this + 0x3a0) + 0xf8))(1);
        DuiLib::CDuiString::Format(this_02,(wchar_t *)local_98,&DAT_00424f54,local_a8);
        pcVar4 = operator_wchar_t_const__exref;
        iVar2 = **(int **)((int)local_a0 + 0x3a4);
        pwVar1 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
        (**(code **)(iVar2 + 0x2c))(pwVar1);
        DuiLib::CDuiString::Format(this_03,(wchar_t *)local_98,&DAT_00424f54,local_ac);
        iVar2 = **(int **)((int)local_a0 + 0x3a8);
        pwVar1 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
        (**(code **)(iVar2 + 0x2c))(pwVar1);
        DuiLib::CDuiString::Format
                  (local_a4,(wchar_t *)local_98,&DAT_00424f54,(uint)*(ushort *)(local_a4 + 0x28));
        this = local_a0;
      }
      else {
        (**(code **)(iVar2 + 0xf8))(1);
        (**(code **)(**(int **)((int)this + 0x3a0) + 0xf8))(0);
        (**(code **)(**(int **)((int)this + 0x374) + 0xf8))(1);
        (**(code **)(**(int **)((int)this + 900) + 0xf8))(0);
        pCVar3 = FUN_00402370(local_130,(uint)(byte)local_99);
        local_8._0_1_ = 1;
        DuiLib::CDuiString::operator=(local_98,pCVar3);
        local_8 = (uint)local_8._1_3_ << 8;
        DuiLib::CDuiString::~CDuiString(local_130);
        pcVar4 = operator_wchar_t_const__exref;
        pwVar1 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
        pCVar3 = local_130;
        this_00 = DuiLib::CResourceManager::GetInstance();
        pCVar3 = (CDuiString *)DuiLib::CResourceManager::GetText(this_00,(wchar_t *)pCVar3,pwVar1);
        local_8._0_1_ = 2;
        DuiLib::CDuiString::operator=(local_98,pCVar3);
        local_8 = (uint)local_8._1_3_ << 8;
        DuiLib::CDuiString::~CDuiString(local_130);
        iVar2 = **(int **)((int)this + 0x374);
        pwVar1 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
        (**(code **)(iVar2 + 0x2c))(pwVar1);
        DuiLib::CDuiString::Format
                  (local_a4,(wchar_t *)local_98,&DAT_00424f54,(uint)*(ushort *)(local_a4 + 0x28));
      }
      iVar2 = **(int **)((int)this + 0x378);
      pwVar1 = (wchar_t *)(*pcVar4)();
    }
    (**(code **)(iVar2 + 0x2c))(pwVar1);
    DuiLib::CDuiString::~CDuiString(local_98);
  }
  ExceptionList = local_10;
  return;
}


