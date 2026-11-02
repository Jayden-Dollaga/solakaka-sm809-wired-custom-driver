// Program: SM809 mouse Software.exe
// Function: FUN_00410d10
// Entry: 00410d10
// Body: 00410d10 - 004111a0
// Signature: undefined FUN_00410d10(void * this, UINT param_1, int param_2)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_00410d10(void *this,UINT param_1,int param_2)

{
  undefined4 uVar1;
  void *this_00;
  ushort uVar2;
  uint uVar3;
  int iVar4;
  DWORD DVar5;
  CDuiString *pCVar6;
  wchar_t *pwVar7;
  CResourceManager *this_01;
  undefined2 uVar8;
  uint uVar9;
  longlong lVar10;
  undefined8 uVar11;
  CDuiString local_1b8 [132];
  undefined4 local_134;
  undefined4 uStack_130;
  undefined4 uStack_12c;
  undefined4 uStack_128;
  void *local_124;
  int local_120;
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00422925;
  local_10 = ExceptionList;
  uVar3 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  if ((DAT_00432a9c == param_1) && (DAT_00432a98 == param_2)) {
    return;
  }
  DAT_00432a9c = param_1;
  DAT_00432a98 = param_2;
  ExceptionList = &local_10;
  local_124 = this;
  local_14 = uVar3;
  DuiLib::CDuiString::CDuiString(local_11c);
  local_8 = 0;
  if (param_1 == 0x20a) goto LAB_00411178;
  if (param_1 == 0x201) {
    local_120 = 0xf0;
    param_2 = 0;
  }
  else if (param_1 == 0x202) {
    local_120 = 0xf0;
    param_2 = 1;
  }
  else if (param_1 == 0x204) {
    local_120 = 0xf1;
    param_2 = 0;
  }
  else if (param_1 == 0x205) {
    local_120 = 0xf1;
    param_2 = 1;
  }
  else if (param_1 == 0x207) {
    local_120 = 0xf2;
    param_2 = 0;
  }
  else if (param_1 == 0x208) {
    local_120 = 0xf2;
    param_2 = 1;
  }
  else if (param_1 == 0x20b) {
    if (param_2 == 2) {
      local_120 = 0xf4;
      param_2 = 0;
    }
    else {
      if (param_2 != 1) goto LAB_00410ea3;
      local_120 = 0xf3;
      param_2 = 0;
    }
  }
  else if (param_1 == 0x20c) {
    if (param_2 == 2) {
      local_120 = 0xf4;
      param_2 = 1;
    }
    else {
      if (param_2 != 1) goto LAB_00410ea3;
      local_120 = 0xf3;
    }
  }
  else {
LAB_00410ea3:
    FUN_004022f0(param_1,&local_120);
  }
  if (*(int *)((int)this + 0x2a8) == 0) {
    if (-1 < *(int *)((int)this + 700)) {
      DuiLib::CDuiString::CDuiString(local_98);
      local_8._0_1_ = 1;
      pCVar6 = FUN_00402370(local_1b8,local_120);
      local_8._0_1_ = 2;
      DuiLib::CDuiString::operator=(local_98,pCVar6);
      local_8._0_1_ = 1;
      DuiLib::CDuiString::~CDuiString(local_1b8);
      pwVar7 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
      pCVar6 = local_1b8;
      this_01 = DuiLib::CResourceManager::GetInstance();
      pCVar6 = (CDuiString *)DuiLib::CResourceManager::GetText(this_01,(wchar_t *)pCVar6,pwVar7);
      local_8._0_1_ = 3;
      DuiLib::CDuiString::operator=(local_98,pCVar6);
      local_8 = CONCAT31(local_8._1_3_,1);
      DuiLib::CDuiString::~CDuiString(local_1b8);
      iVar4 = **(int **)((int)local_124 + 0x374);
      pwVar7 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
      this_00 = local_124;
      (**(code **)(iVar4 + 0x2c))(pwVar7);
      *(char *)((int)this_00 + *(int *)((int)this_00 + 700) * 0x10 + 0x25) = (char)local_120;
      FUN_00411ae0(this_00,*(int *)((int)this_00 + 700));
      FUN_004116c0((int)this_00);
      DuiLib::CDuiString::~CDuiString(local_98);
    }
  }
  else {
    uVar9 = 10;
    uVar8 = 10;
    if (*(int *)((int)this + 0x2ac) != 0) {
      if (*(int *)((int)this + 0x20) == 2) {
        if (*(int *)((int)this + 0x2ec) == 0) {
          DVar5 = GetTickCount();
          uVar2 = (short)DVar5 - *(short *)((int)this + 0x2c8);
          *(ushort *)((int)this + 0x2c4) = uVar2;
          uVar9 = (uint)uVar2;
        }
        else {
          QueryPerformanceCounter((LARGE_INTEGER *)((int)this + 0x2e0));
          uVar9 = (((LARGE_INTEGER *)((int)this + 0x2e0))->s).LowPart;
          lVar10 = __allmul(uVar9 - *(uint *)((int)this + 0x2d8),
                            (*(int *)((int)this + 0x2e4) - *(int *)((int)this + 0x2dc)) -
                            (uint)(uVar9 < *(uint *)((int)this + 0x2d8)),1000000,0);
          uVar11 = __alldiv((uint)lVar10,(uint)((ulonglong)lVar10 >> 0x20),
                            *(uint *)((int)this + 0x2d0),*(uint *)((int)this + 0x2d4));
          *(int *)((int)this + 0x2e8) = (int)uVar11;
          uVar9 = ((int)uVar11 + 500) / 1000;
        }
        if (0xfffe < (int)uVar9) {
          uVar9 = 0xffff;
        }
      }
      else if (*(int *)((int)this + 0x20) == 1) {
        uVar9 = (uint)*(ushort *)((int)this + 0x2b8);
      }
      iVar4 = *(int *)((int)this + 0x2b4);
      uVar8 = (undefined2)uVar9;
      if (iVar4 == -1) {
        if (*(int *)((int)this + 0x2a4) - 1U < 0x28) {
          *(undefined2 *)((int)this + *(int *)((int)this + 0x2a4) * 0x10 + 0x18) = uVar8;
        }
      }
      else if (*(int *)((int)this + 0x2b0) == iVar4) {
        *(undefined2 *)((int)this + iVar4 * 0x10 + 0x28) = uVar8;
      }
      else {
        *(undefined2 *)((int)this + iVar4 * 0x10 + 0x18) = uVar8;
      }
    }
    DuiLib::DUI__Trace(L"m_iInsertPosTmp1 = %d\r\n",*(undefined4 *)((int)this + 0x2b4),uVar3);
    uVar1 = local_134;
    uStack_130 = CONCAT22(uStack_130._2_2_,uVar8);
    local_134._0_2_ = CONCAT11((char)local_120,(undefined1)local_134);
    local_134._3_1_ = SUB41(uVar1,3);
    local_134._0_3_ = CONCAT12(2,(undefined2)local_134);
    if (param_2 == 0) {
      local_134._0_3_ = CONCAT12(1,(undefined2)local_134);
    }
    FUN_004111b0(this,local_134,uStack_130,uStack_12c,uStack_128);
    iVar4 = *(int *)((int)this + 0x2b4);
    if (iVar4 == -1) {
      iVar4 = *(int *)((int)this + 0x2a4);
    }
    *(undefined2 *)((int)this + iVar4 * 0x10 + 0x18) = 10;
    DuiLib::DUI__Trace(L"m_iInsertPosTmp2 = %d\r\n",*(undefined4 *)((int)this + 0x2b4));
    if (*(int *)((int)this + 0x2ec) == 0) {
      DVar5 = GetTickCount();
      *(DWORD *)((int)this + 0x2c8) = DVar5;
    }
    else {
      QueryPerformanceCounter((LARGE_INTEGER *)((int)this + 0x2d8));
    }
    *(undefined4 *)((int)this + 0x2ac) = 1;
    if (0x27 < *(int *)((int)this + 0x2a4)) {
      FUN_00410ca0((int)this);
    }
    FUN_00411220((int)this);
  }
LAB_00411178:
  DuiLib::CDuiString::~CDuiString(local_11c);
  ExceptionList = local_10;
  return;
}


