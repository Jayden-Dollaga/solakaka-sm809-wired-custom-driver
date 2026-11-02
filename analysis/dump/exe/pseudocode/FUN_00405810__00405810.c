// Program: SM809 mouse Software.exe
// Function: FUN_00405810
// Entry: 00405810
// Body: 00405810 - 004058fe
// Signature: _Facet_base * FUN_00405810(locale * param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

_Facet_base * __fastcall FUN_00405810(locale *param_1)

{
  int iVar1;
  uint uVar2;
  _Locimp *p_Var3;
  _Facet_base *p_Var4;
  _Facet_base *local_20;
  _Facet_base *local_1c;
  _Lockit local_18 [4];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_004215b6;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_18 + 0x14);
  ExceptionList = &local_10;
  std::_Lockit::_Lockit(local_18,0);
  local_8 = 0;
  local_20 = DAT_00432a80;
  uVar2 = std::locale::id::operator_unsigned_int((id *)id_exref);
  iVar1 = *(int *)(param_1 + 4);
  if (uVar2 < *(uint *)(iVar1 + 0xc)) {
    p_Var4 = *(_Facet_base **)(*(int *)(iVar1 + 8) + uVar2 * 4);
    if (p_Var4 != (_Facet_base *)0x0) goto LAB_004058d3;
  }
  else {
    p_Var4 = (_Facet_base *)0x0;
  }
  if (*(char *)(iVar1 + 0x14) == '\0') {
LAB_00405892:
    if (p_Var4 != (_Facet_base *)0x0) goto LAB_004058d3;
  }
  else {
    p_Var3 = std::locale::_Getgloballocale();
    if (uVar2 < *(uint *)(p_Var3 + 0xc)) {
      p_Var4 = *(_Facet_base **)(*(int *)(p_Var3 + 8) + uVar2 * 4);
      goto LAB_00405892;
    }
  }
  p_Var4 = local_20;
  if (local_20 == (_Facet_base *)0x0) {
    uVar2 = std::codecvt<char,char,_Mbstatet>::_Getcat((facet **)&local_20,param_1);
    p_Var4 = local_20;
    if (uVar2 == 0xffffffff) {
                    /* WARNING: Subroutine does not return */
      FUN_004059e0();
    }
    local_1c = local_20;
    local_8 = CONCAT31(local_8._1_3_,1);
    std::_Facet_Register(local_20);
    (**(code **)(*(int *)p_Var4 + 4))();
    DAT_00432a80 = local_20;
    p_Var4 = local_20;
  }
LAB_004058d3:
  std::_Lockit::~_Lockit(local_18);
  ExceptionList = local_10;
  return p_Var4;
}


