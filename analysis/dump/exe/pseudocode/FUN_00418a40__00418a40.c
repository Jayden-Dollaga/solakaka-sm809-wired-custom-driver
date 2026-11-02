// Program: SM809 mouse Software.exe
// Function: FUN_00418a40
// Entry: 00418a40
// Body: 00418a40 - 00419462
// Signature: undefined FUN_00418a40(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_00418a40(int param_1)

{
  void *pvVar1;
  undefined4 uVar2;
  char cVar3;
  char cVar4;
  undefined4 uVar5;
  int iVar6;
  CControlUI *pCVar7;
  char cVar8;
  uint uVar9;
  UINT uiParam;
  code *pcVar10;
  bool bVar11;
  uint uStack_1bc;
  uint uStack_1b8;
  int iStack_1b4;
  int iStack_1b0;
  uint local_1ac [3];
  undefined4 local_1a0;
  undefined4 local_19c;
  undefined4 uStack_198;
  undefined4 uStack_194;
  undefined4 uStack_190;
  undefined4 uStack_18c;
  undefined4 uStack_188;
  undefined4 uStack_184;
  undefined4 uStack_d8;
  undefined4 uStack_d4;
  undefined4 uStack_d0;
  undefined4 uStack_cc;
  undefined4 uStack_c8;
  undefined4 uStack_c4;
  undefined4 uStack_c0;
  undefined4 uStack_bc;
  undefined1 auStack_b8 [172];
  uint local_c;
  
  pvVar1 = DAT_00432aa0;
  local_c = DAT_00432008 ^ (uint)&uStack_1bc;
  pcVar10 = SystemParametersInfoW_exref;
  if (*(int *)((int)DAT_00432aa0 + 0x6c) != DAT_0044f79c) {
    uiParam = *(int *)((int)DAT_00432aa0 + 0x6c) * -0x46 + 900;
    SetDoubleClickTime(uiParam);
    pcVar10 = SystemParametersInfoW_exref;
    SystemParametersInfoW(0x20,uiParam,(PVOID)0x0,3);
  }
  if ((*(int *)((int)pvVar1 + 100) != DAT_0044f794) ||
     (*(int *)((int)pvVar1 + 0x70) != DAT_0044f7a0)) {
    bVar11 = *(int *)((int)pvVar1 + 0x70) != 0;
    if (bVar11) {
      local_1ac[2] = 10;
      local_1ac[1] = 6;
    }
    else {
      local_1ac[2] = 0;
      local_1ac[1] = 0;
    }
    local_1ac[0] = (uint)bVar11;
    (*pcVar10)(4,0,local_1ac,3);
    switch(*(undefined4 *)((int)pvVar1 + 100)) {
    case 1:
      uVar5 = 1;
      break;
    case 2:
      uVar5 = 2;
      break;
    case 3:
      uVar5 = 4;
      break;
    case 4:
      uVar5 = 6;
      break;
    case 5:
      uVar5 = 8;
      break;
    default:
      uVar5 = 10;
      break;
    case 7:
      uVar5 = 0xc;
      break;
    case 8:
      uVar5 = 0xe;
      break;
    case 9:
      uVar5 = 0x10;
      break;
    case 10:
      uVar5 = 0x12;
      break;
    case 0xb:
      uVar5 = 0x14;
    }
    (*pcVar10)(0x71,0,uVar5,3);
  }
  if ((*(int *)((int)pvVar1 + 0x68) != DAT_0044f798) ||
     (*(int *)((int)pvVar1 + 0x74) != DAT_0044f7a4)) {
    iVar6 = -1;
    if (*(int *)((int)pvVar1 + 0x74) == 0) {
      iVar6 = *(int *)((int)pvVar1 + 0x68);
    }
    (*pcVar10)(0x69,iVar6,iVar6,3);
  }
  memcpy(&DAT_0044f730,DAT_00432aa0,0x1cc50);
  FUN_004196b0(param_1);
  memset(&local_1a0,0,100);
  cVar8 = *(char *)((int)DAT_00432aa0 + 0x14c) + '\x01';
  local_1a0._0_2_ = CONCAT11(cVar8,2);
  local_1a0 = (uint)(ushort)local_1a0;
  cVar8 = (((-3 - local_19c._2_1_) - cVar8) - (char)local_19c) - local_19c._1_1_;
  local_19c = CONCAT13(cVar8,(undefined3)local_19c);
  if (*(int *)(param_1 + 0x1af0) != 0) {
    FUN_00414710((byte *)&local_1a0);
  }
  iVar6 = (**(code **)(param_1 + 0x788))(&local_1a0,8);
  if (iVar6 != 0) {
    Sleep(0x14);
  }
  switch(*(undefined4 *)((int)DAT_00432aa0 + 0x80)) {
  case 0:
    cVar8 = '\b';
    break;
  case 1:
    cVar8 = '\x04';
    break;
  default:
    cVar8 = '\x02';
    break;
  case 3:
    cVar8 = '\x01';
  }
  memset(&local_1a0,0,100);
  cVar3 = ((-2 - local_19c._2_1_) - (char)local_19c) - local_19c._1_1_;
  local_1a0._0_2_ = CONCAT11(cVar8,1);
  local_1a0 = (uint)(ushort)local_1a0;
  local_19c = CONCAT13(cVar3 - cVar8,(undefined3)local_19c);
  if (*(int *)(param_1 + 0x1af0) != 0) {
    FUN_00414710((byte *)&local_1a0);
  }
  iVar6 = (**(code **)(param_1 + 0x788))(&local_1a0,8);
  if (iVar6 != 0) {
    Sleep(0x14);
  }
  memset(&uStack_d8,0,200);
  cVar3 = *(char *)((int)DAT_00432aa0 + 0x84) + '\x01';
  cVar8 = ((((-0xc - uStack_d4._2_1_) - uStack_d8._2_1_) - uStack_d8._3_1_) - (char)uStack_d4) -
          uStack_d4._1_1_;
  uStack_d8._0_2_ = CONCAT11(cVar3,0xb);
  uStack_d4 = CONCAT13(cVar8 - cVar3,(undefined3)uStack_d4);
  if (*(int *)(param_1 + 0x1af0) != 0) {
    FUN_00414710((byte *)&uStack_d8);
  }
  iVar6 = (**(code **)(param_1 + 0x788))(&uStack_d8,8);
  if (iVar6 != 0) {
    Sleep(0x14);
  }
  memset(&local_1a0,0,200);
  cVar8 = ((-0xd - local_19c._2_1_) - (char)local_19c) - local_19c._1_1_;
  local_1a0._0_2_ = CONCAT11(*(char *)((int)DAT_00432aa0 + 0x104),0xc);
  local_1a0._0_3_ = CONCAT12(*(char *)((int)DAT_00432aa0 + 0x105),(ushort)local_1a0);
  local_1a0 = CONCAT13(*(char *)((int)DAT_00432aa0 + 0x106),(undefined3)local_1a0);
  local_19c = CONCAT13(((cVar8 - *(char *)((int)DAT_00432aa0 + 0x106)) -
                       *(char *)((int)DAT_00432aa0 + 0x105)) - *(char *)((int)DAT_00432aa0 + 0x104),
                       (undefined3)local_19c);
  if (*(int *)(param_1 + 0x1af0) != 0) {
    FUN_00414710((byte *)&local_1a0);
  }
  iVar6 = (**(code **)(param_1 + 0x788))(&local_1a0,8);
  if (iVar6 != 0) {
    Sleep(0x14);
  }
  iStack_1b4 = *(int *)((int)DAT_00432aa0 + 0xf0);
  uVar9 = *(uint *)((int)DAT_00432aa0 + 0xfc);
  uStack_1bc = *(uint *)((int)DAT_00432aa0 + 0xf4);
  iStack_1b0 = 4 - *(int *)((int)DAT_00432aa0 + 0x100);
  uStack_1b8 = 4 - *(int *)((int)DAT_00432aa0 + 0xf8);
  if (uVar9 == 1) {
    uVar9 = 2;
  }
  memset(&local_1a0,0,200);
  uVar5 = local_1a0;
  local_1a0._0_2_ = CONCAT11((char)iStack_1b4,0xd);
  uVar2 = local_1a0;
  if (iStack_1b4 == 0) {
    local_1a0 = 0xd;
    cVar3 = '\0';
    cVar8 = '\0';
    goto LAB_00418e77;
  }
  if (iStack_1b4 == 1) goto LAB_00418e6b;
  if (iStack_1b4 == 2) {
    cVar8 = '\x04' - (char)uStack_1b8;
  }
  else if ((iStack_1b4 == 3) || (iStack_1b4 == 4)) {
    uVar9 = uStack_1bc & 0xff;
    cVar8 = '\x04' - (char)uStack_1b8;
  }
  else {
    if (iStack_1b4 != 5) {
      if ((iStack_1b4 == 6) || (iStack_1b4 == 7)) {
        cVar8 = (char)iStack_1b0;
        goto LAB_00418e6f;
      }
      if (iStack_1b4 == 8) {
        uVar9 = (uint)(uVar9 != 0);
      }
      else if (iStack_1b4 == 9) {
        uVar9 = (uint)(byte)((byte)uVar9 | (char)uStack_1b8 << 4);
      }
      else if (iStack_1b4 == 10) {
        uVar9 = uStack_1b8 & 0xff;
      }
      else if (iStack_1b4 != 0xb) {
        local_1a0._3_1_ = SUB41(uVar5,3);
        local_1a0._2_1_ = SUB41(uVar5,2);
        cVar3 = local_1a0._3_1_;
        cVar8 = local_1a0._2_1_;
        local_1a0 = uVar2;
        goto LAB_00418e77;
      }
    }
LAB_00418e6b:
    cVar8 = (char)uStack_1bc;
  }
LAB_00418e6f:
  local_1a0._0_3_ = CONCAT12(cVar8,(ushort)local_1a0);
  local_1a0 = CONCAT13((char)uVar9,(undefined3)local_1a0);
  cVar3 = (char)uVar9;
LAB_00418e77:
  cVar4 = ((-0xe - local_19c._2_1_) - (char)local_19c) - local_19c._1_1_;
  local_19c = CONCAT13(((cVar4 - cVar3) - cVar8) - (char)iStack_1b4,(undefined3)local_19c);
  if (*(int *)(param_1 + 0x1af0) != 0) {
    FUN_00414710((byte *)&local_1a0);
  }
  iVar6 = (**(code **)(param_1 + 0x788))(&local_1a0,8);
  if (iVar6 != 0) {
    Sleep(0x14);
  }
  memset(&uStack_d8,0,200);
  cVar8 = (((-0x29 - uStack_d4._2_1_) - uStack_d8._3_1_) - (char)uStack_d4) - uStack_d4._1_1_;
  uStack_d8 = CONCAT13(uStack_d8._3_1_,0x180010);
  uStack_d4 = CONCAT13(cVar8,(undefined3)uStack_d4);
  if (*(int *)(param_1 + 0x1af0) != 0) {
    FUN_00414710((byte *)&uStack_d8);
  }
  (**(code **)(param_1 + 0x788))(&uStack_d8,8);
  Sleep(0x14);
  memset(&uStack_188,0,0x68);
  local_1a0 = CONCAT13(*(undefined1 *)((int)DAT_00432aa0 + 0x114),
                       *(undefined3 *)((int)DAT_00432aa0 + 0x110));
  local_19c._0_3_ =
       CONCAT12(*(undefined1 *)((int)DAT_00432aa0 + 0x118),
                *(undefined2 *)((int)DAT_00432aa0 + 0x115));
  local_19c = CONCAT13(*(undefined1 *)((int)DAT_00432aa0 + 0x119),(undefined3)local_19c);
  uStack_198._0_2_ =
       CONCAT11(*(undefined1 *)((int)DAT_00432aa0 + 0x11c),
                *(undefined1 *)((int)DAT_00432aa0 + 0x11a));
  uStack_198._0_3_ = CONCAT12(*(undefined1 *)((int)DAT_00432aa0 + 0x11d),(undefined2)uStack_198);
  uStack_198 = CONCAT13(*(undefined1 *)((int)DAT_00432aa0 + 0x11e),(undefined3)uStack_198);
  uStack_194 = CONCAT13(*(undefined1 *)((int)DAT_00432aa0 + 0x124),
                        *(undefined3 *)((int)DAT_00432aa0 + 0x120));
  uStack_190._0_3_ =
       CONCAT12(*(undefined1 *)((int)DAT_00432aa0 + 0x128),
                *(undefined2 *)((int)DAT_00432aa0 + 0x125));
  uStack_190 = CONCAT13(*(undefined1 *)((int)DAT_00432aa0 + 0x129),(undefined3)uStack_190);
  uStack_18c._0_2_ =
       CONCAT11(*(undefined1 *)((int)DAT_00432aa0 + 300),*(undefined1 *)((int)DAT_00432aa0 + 0x12a))
  ;
  uStack_18c._0_3_ = CONCAT12(*(undefined1 *)((int)DAT_00432aa0 + 0x12d),(undefined2)uStack_18c);
  uStack_18c = CONCAT13(*(undefined1 *)((int)DAT_00432aa0 + 0x12e),(undefined3)uStack_18c);
  memset(auStack_b8,0,0xa8);
  uStack_d8 = local_1a0;
  uStack_d4 = local_19c;
  uStack_d0 = uStack_198;
  uStack_cc = uStack_194;
  uStack_c8 = uStack_190;
  uStack_c4 = uStack_18c;
  uStack_c0 = uStack_188;
  uStack_bc = uStack_184;
  (**(code **)(param_1 + 0x798))(&uStack_d8,0x20);
  Sleep(0x14);
  memset(&uStack_d8,0,200);
  cVar8 = (((-0x2a - uStack_d4._2_1_) - uStack_d8._3_1_) - (char)uStack_d4) - uStack_d4._1_1_;
  uStack_d8 = CONCAT13(uStack_d8._3_1_,0x180110);
  uStack_d4 = CONCAT13(cVar8,(undefined3)uStack_d4);
  if (*(int *)(param_1 + 0x1af0) != 0) {
    FUN_00414710((byte *)&uStack_d8);
  }
  (**(code **)(param_1 + 0x788))(&uStack_d8,8);
  Sleep(0x14);
  memset(&uStack_188,0,0x68);
  local_1a0 = CONCAT13(*(undefined1 *)((int)DAT_00432aa0 + 0xd4),
                       *(undefined3 *)((int)DAT_00432aa0 + 0xd0));
  local_19c._0_3_ =
       CONCAT12(*(undefined1 *)((int)DAT_00432aa0 + 0xd8),*(undefined2 *)((int)DAT_00432aa0 + 0xd5))
  ;
  local_19c = CONCAT13(*(undefined1 *)((int)DAT_00432aa0 + 0xd9),(undefined3)local_19c);
  uStack_198._0_2_ =
       CONCAT11(*(undefined1 *)((int)DAT_00432aa0 + 0xdc),*(undefined1 *)((int)DAT_00432aa0 + 0xda))
  ;
  uStack_198._0_3_ = CONCAT12(*(undefined1 *)((int)DAT_00432aa0 + 0xdd),(undefined2)uStack_198);
  uStack_198 = CONCAT13(*(undefined1 *)((int)DAT_00432aa0 + 0xde),(undefined3)uStack_198);
  uStack_194 = CONCAT13(*(undefined1 *)((int)DAT_00432aa0 + 0xe4),
                        *(undefined3 *)((int)DAT_00432aa0 + 0xe0));
  uStack_190._0_3_ =
       CONCAT12(*(undefined1 *)((int)DAT_00432aa0 + 0xe8),*(undefined2 *)((int)DAT_00432aa0 + 0xe5))
  ;
  uStack_190 = CONCAT13(*(undefined1 *)((int)DAT_00432aa0 + 0xe9),(undefined3)uStack_190);
  uStack_18c._0_2_ =
       CONCAT11(*(undefined1 *)((int)DAT_00432aa0 + 0xec),*(undefined1 *)((int)DAT_00432aa0 + 0xea))
  ;
  uStack_18c._0_3_ = CONCAT12(*(undefined1 *)((int)DAT_00432aa0 + 0xed),(undefined2)uStack_18c);
  uStack_18c = CONCAT13(*(undefined1 *)((int)DAT_00432aa0 + 0xee),(undefined3)uStack_18c);
  memset(auStack_b8,0,0xa8);
  uStack_d8 = local_1a0;
  uStack_d4 = local_19c;
  uStack_d0 = uStack_198;
  uStack_cc = uStack_194;
  uStack_c8 = uStack_190;
  uStack_c4 = uStack_18c;
  uStack_c0 = uStack_188;
  uStack_bc = uStack_184;
  (**(code **)(param_1 + 0x798))(&uStack_d8,0x20);
  Sleep(0x14);
  FUN_00419860(param_1);
  FUN_0041ab50(param_1);
  memset(&uStack_d8,0,200);
  uVar5 = uStack_d8;
  uStack_d8 = CONCAT31(uStack_d8._1_3_,4);
  uVar2 = uStack_d8;
  if (*(uint *)((int)DAT_00432aa0 + 0x130) < 8) {
    cVar8 = *(char *)(*(uint *)((int)DAT_00432aa0 + 0x130) + 0x16c8 + param_1);
    uStack_d8._2_2_ = SUB42(uVar5,2);
    uStack_d8._0_2_ = CONCAT11(cVar8,4);
  }
  else {
    uStack_d8._1_1_ = SUB41(uVar5,1);
    cVar8 = uStack_d8._1_1_;
    uStack_d8 = uVar2;
  }
  uStack_d8._0_3_ = CONCAT12(*(char *)((int)DAT_00432aa0 + 0x138),(undefined2)uStack_d8);
  cVar3 = ((((-5 - *(char *)((int)DAT_00432aa0 + 0x138)) - uStack_d4._2_1_) - uStack_d8._3_1_) -
          (char)uStack_d4) - uStack_d4._1_1_;
  uStack_d4 = CONCAT13(cVar3 - cVar8,(undefined3)uStack_d4);
  if (*(int *)(param_1 + 0x1af0) != 0) {
    FUN_00414710((byte *)&uStack_d8);
  }
  if (DAT_00432acc != 0) {
    (**(code **)(param_1 + 0x788))(&uStack_d8,8);
  }
  Sleep(0x14);
  memset(&uStack_d8,0,200);
  uStack_d8 = 0xeeccaa08;
  cVar8 = ((-0x6d - uStack_d4._2_1_) - (char)uStack_d4) - uStack_d4._1_1_;
  uStack_d4 = CONCAT13(cVar8,(undefined3)uStack_d4);
  if (*(int *)(param_1 + 0x1af0) != 0) {
    FUN_00414710((byte *)&uStack_d8);
  }
  (**(code **)(param_1 + 0x788))(&uStack_d8,8);
  Sleep(0x14);
  if (((DAT_00432ad8 == 0xd07) || (DAT_00432ad8 == 0xd2a)) || (DAT_00432ad8 == 0xcef)) {
    FUN_0041bd40(param_1);
  }
  FUN_00402b20();
  FUN_004035a0();
  pCVar7 = DuiLib::CPaintManagerUI::FindControl((CPaintManagerUI *)(param_1 + 0x30),L"ring_ver");
  (**(code **)(*(int *)pCVar7 + 0xf8))(0);
  return;
}


