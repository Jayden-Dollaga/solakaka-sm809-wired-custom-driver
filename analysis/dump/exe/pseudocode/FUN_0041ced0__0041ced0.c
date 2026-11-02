// Program: SM809 mouse Software.exe
// Function: FUN_0041ced0
// Entry: 0041ced0
// Body: 0041ced0 - 0041d016
// Signature: undefined FUN_0041ced0(void * this, int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_0041ced0(void *this,int param_1)

{
  byte bVar1;
  int iVar2;
  uint uVar3;
  wchar_t *pwVar4;
  int *piVar5;
  CDuiString *pCVar6;
  CDuiString *this_00;
  int iVar7;
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00421b3d;
  local_10 = ExceptionList;
  uVar3 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  iVar2 = *(int *)(param_1 + 0x108);
  if (((iVar2 != *(int *)((int)this + 0x108)) && (iVar2 != *(int *)((int)this + 0x10c))) &&
     (iVar2 != *(int *)((int)this + 0x110))) {
    local_14 = uVar3;
    if (iVar2 == *(int *)((int)this + 300)) {
      bVar1 = *(byte *)(param_1 + 0x118);
      *(byte *)(DAT_00432aa0 + 0x138) = bVar1;
      DuiLib::CDuiString::CDuiString(local_98);
      local_8 = 0;
      DuiLib::CDuiString::Format(this_00,(wchar_t *)local_98,L"%d ms",(uint)bVar1);
      iVar2 = **(int **)((int)this + 0x130);
      pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(local_98);
      (**(code **)(iVar2 + 0x2c))(pwVar4);
      pCVar6 = local_98;
LAB_0041cff4:
      DuiLib::CDuiString::~CDuiString(pCVar6);
    }
    else {
      iVar7 = 0;
      piVar5 = (int *)((int)this + 0x68);
      do {
        if (iVar2 == *piVar5) {
          iVar2 = *(int *)(param_1 + 0x118);
          *(int *)(DAT_00432aa0 + 0x88 + iVar7 * 4) = iVar2;
          pCVar6 = FUN_00403d70(local_11c,iVar2);
          local_8 = 1;
          iVar2 = **(int **)((int)this + iVar7 * 4 + 0x48);
          pwVar4 = DuiLib::CDuiString::operator_wchar_t_const_(pCVar6);
          (**(code **)(iVar2 + 0x2c))(pwVar4,uVar3);
          pCVar6 = local_11c;
          goto LAB_0041cff4;
        }
        iVar7 = iVar7 + 1;
        piVar5 = piVar5 + 1;
      } while (iVar7 < 8);
    }
  }
  ExceptionList = local_10;
  return;
}


