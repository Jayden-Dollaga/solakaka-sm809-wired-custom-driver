// Program: SM809 mouse Software.exe
// Function: FUN_00419860
// Entry: 00419860
// Body: 00419860 - 0041aacf
// Signature: int FUN_00419860(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

int __fastcall FUN_00419860(int param_1)

{
  byte bVar1;
  byte bVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  uint uVar6;
  int iVar7;
  int iVar8;
  char cVar9;
  undefined2 uVar10;
  byte bVar12;
  int iVar11;
  byte bVar13;
  byte bVar14;
  undefined4 *puVar15;
  code *pcVar16;
  bool bVar17;
  bool bVar18;
  byte local_13d;
  undefined4 local_13c;
  undefined4 local_138;
  undefined1 local_134 [192];
  undefined4 local_74;
  undefined4 local_70;
  undefined4 local_8;
  
  local_8 = DAT_00432008 ^ (uint)(local_134 + 0x130);
  memset(&local_13c,0,200);
  cVar9 = local_13c._3_1_;
  local_13c = CONCAT13(local_13c._3_1_,0x80000);
  local_13c._0_2_ = CONCAT11(*(char *)(DAT_00432aa0 + 0x139),0x11);
  cVar9 = ((((-0x1a - *(char *)(DAT_00432aa0 + 0x139)) - local_138._2_1_) - cVar9) - (char)local_138
          ) - local_138._1_1_;
  local_138 = CONCAT13(cVar9,(undefined3)local_138);
  if (*(int *)(param_1 + 0x1af0) != 0) {
    FUN_00414710((byte *)&local_13c);
  }
  (**(code **)(param_1 + 0x788))(&local_13c,8);
  pcVar16 = Sleep_exref;
  Sleep(0x14);
  uVar3 = 0;
  bVar13 = 0;
  memset(&local_74,0,100);
  if (DAT_00432ad8 == 0xcfd) {
    if (*(char *)(DAT_00432aa0 + 200) == '\0') {
      uVar10 = 0x8000;
    }
    else {
      iVar8 = *(int *)(DAT_00432aa0 + 0x88);
      uVar10 = 0;
      if (0x32 < iVar8) {
        uVar10 = 0x40;
        iVar8 = iVar8 / 2;
      }
      bVar13 = (char)iVar8 - 1;
    }
    bVar14 = (byte)uVar10;
    bVar1 = bVar13 | bVar14;
    if (*(char *)(DAT_00432aa0 + 0xc9) == '\0') {
      bVar2 = 0x80;
    }
    else {
      iVar8 = *(int *)(DAT_00432aa0 + 0x8c);
      bVar14 = 0;
      bVar2 = 0;
      if (iVar8 < 0x33) {
        bVar13 = (char)iVar8 - 1;
      }
      else {
        bVar14 = 0x40;
        bVar2 = 0;
        bVar13 = (char)(iVar8 / 2) - 1;
      }
    }
    local_74._0_2_ = CONCAT11(bVar13 | bVar14 | bVar2,bVar1 | (byte)((ushort)uVar10 >> 8));
    if (*(char *)(DAT_00432aa0 + 0xca) == '\0') {
      bVar1 = 0x80;
    }
    else {
      iVar8 = *(int *)(DAT_00432aa0 + 0x90);
      bVar14 = 0;
      bVar1 = 0;
      if (iVar8 < 0x33) {
        bVar13 = (char)iVar8 - 1;
      }
      else {
        bVar14 = 0x40;
        bVar1 = 0;
        bVar13 = (char)(iVar8 / 2) - 1;
      }
    }
    local_74._0_3_ = CONCAT12(bVar13 | bVar14 | bVar1,(undefined2)local_74);
    if (*(char *)(DAT_00432aa0 + 0xcb) == '\0') {
      bVar1 = 0x80;
    }
    else {
      iVar8 = *(int *)(DAT_00432aa0 + 0x94);
      bVar14 = 0;
      bVar1 = 0;
      if (iVar8 < 0x33) {
        bVar13 = (char)iVar8 - 1;
      }
      else {
        bVar14 = 0x40;
        bVar1 = 0;
        bVar13 = (char)(iVar8 / 2) - 1;
      }
    }
    local_74 = CONCAT13(bVar13 | bVar14 | bVar1,(undefined3)local_74);
    if (*(char *)(DAT_00432aa0 + 0xcc) == '\0') {
      bVar1 = 0x80;
    }
    else {
      iVar8 = *(int *)(DAT_00432aa0 + 0x98);
      bVar14 = 0;
      bVar1 = 0;
      if (iVar8 < 0x33) {
        bVar13 = (char)iVar8 - 1;
      }
      else {
        bVar14 = 0x40;
        bVar1 = 0;
        bVar13 = (char)(iVar8 / 2) - 1;
      }
    }
    bVar2 = bVar13 | bVar14;
    if (*(char *)(DAT_00432aa0 + 0xcd) == '\0') {
      bVar12 = 0x80;
    }
    else {
      iVar8 = *(int *)(DAT_00432aa0 + 0x9c);
      bVar14 = 0;
      bVar12 = 0;
      if (iVar8 < 0x33) {
        bVar13 = (char)iVar8 - 1;
      }
      else {
        bVar14 = 0x40;
        bVar12 = 0;
        bVar13 = (char)(iVar8 / 2) - 1;
      }
    }
    local_70._0_2_ = CONCAT11(bVar13 | bVar14 | bVar12,bVar2 | bVar1);
    if (*(char *)(DAT_00432aa0 + 0xce) == '\0') {
      bVar1 = 0x80;
    }
    else {
      iVar8 = *(int *)(DAT_00432aa0 + 0xa0);
      bVar14 = 0;
      bVar1 = 0;
      if (iVar8 < 0x33) {
        bVar13 = (char)iVar8 - 1;
      }
      else {
        bVar14 = 0x40;
        bVar1 = 0;
        bVar13 = (char)(iVar8 / 2) - 1;
      }
    }
    local_70._0_3_ = CONCAT12(bVar13 | bVar14 | bVar1,(undefined2)local_70);
    if (*(char *)(DAT_00432aa0 + 0xcf) == '\0') {
      local_70 = CONCAT13(bVar13 | bVar14,(uint3)local_70) | 0x80000000;
    }
    else {
      iVar8 = *(int *)(DAT_00432aa0 + 0xa4);
      if (iVar8 < 0x33) {
        local_70 = CONCAT13((char)iVar8 + -1,(uint3)local_70);
      }
      else {
        local_70 = CONCAT13((char)(iVar8 / 2) + -1,(uint3)local_70) | 0x40000000;
      }
    }
    goto LAB_0041aa74;
  }
  if (DAT_00432ad8 == 0xc8c) {
    bVar13 = 0;
    iVar8 = *(int *)(DAT_00432aa0 + 0x88);
    if (iVar8 < 0x7f) {
      if (iVar8 - 0x40U < 0x3f) {
        bVar13 = 0x40;
        iVar8 = iVar8 / 2;
      }
    }
    else {
      bVar13 = 0xc0;
      iVar8 = iVar8 / 3;
    }
    bVar1 = 0;
    iVar11 = *(int *)(DAT_00432aa0 + 0x8c);
    if (iVar11 < 0x7f) {
      if (iVar11 - 0x40U < 0x3f) {
        bVar1 = 0x40;
        iVar11 = iVar11 / 2;
      }
    }
    else {
      bVar1 = 0xc0;
      iVar11 = iVar11 / 3;
    }
    bVar14 = 0;
    local_74._0_2_ = CONCAT11((byte)iVar11 | bVar1,(byte)iVar8 | bVar13);
    iVar8 = *(int *)(DAT_00432aa0 + 0x90);
    if (iVar8 < 0x7f) {
      if (iVar8 - 0x40U < 0x3f) {
        bVar14 = 0x40;
        iVar8 = iVar8 / 2;
      }
    }
    else {
      bVar14 = 0xc0;
      iVar8 = iVar8 / 3;
    }
    bVar13 = 0;
    local_74._0_3_ = CONCAT12((byte)iVar8 | bVar14,(undefined2)local_74);
    iVar8 = *(int *)(DAT_00432aa0 + 0x94);
    if (iVar8 < 0x7f) {
      if (iVar8 - 0x40U < 0x3f) {
        bVar13 = 0x40;
        iVar8 = iVar8 / 2;
      }
    }
    else {
      bVar13 = 0xc0;
      iVar8 = iVar8 / 3;
    }
    bVar1 = 0;
    local_74 = CONCAT13((byte)iVar8 | bVar13,(undefined3)local_74);
    iVar8 = *(int *)(DAT_00432aa0 + 0x98);
    if (iVar8 < 0x7f) {
      if (iVar8 - 0x40U < 0x3f) {
        bVar1 = 0x40;
        iVar8 = iVar8 / 2;
      }
    }
    else {
      bVar1 = 0xc0;
      iVar8 = iVar8 / 3;
    }
    bVar13 = 0;
    iVar11 = *(int *)(DAT_00432aa0 + 0x9c);
    if (iVar11 < 0x7f) {
      if (iVar11 - 0x40U < 0x3f) {
        bVar13 = 0x40;
        iVar11 = iVar11 / 2;
      }
    }
    else {
      bVar13 = 0xc0;
      iVar11 = iVar11 / 3;
    }
    bVar14 = 0;
    local_70._0_2_ = CONCAT11((byte)iVar11 | bVar13,(byte)iVar8 | bVar1);
    iVar8 = *(int *)(DAT_00432aa0 + 0xa0);
    if (iVar8 < 0x7f) {
      if (iVar8 - 0x40U < 0x3f) {
        bVar14 = 0x40;
        iVar8 = iVar8 / 2;
      }
    }
    else {
      bVar14 = 0xc0;
      iVar8 = iVar8 / 3;
    }
    bVar13 = 0;
    local_70._0_3_ = CONCAT12((byte)iVar8 | bVar14,(undefined2)local_70);
    iVar8 = *(int *)(DAT_00432aa0 + 0xa4);
    if (iVar8 < 0x7f) {
      if (iVar8 - 0x40U < 0x3f) {
        bVar13 = 0x40;
        iVar8 = iVar8 / 2;
      }
      local_70 = CONCAT13((byte)iVar8 | bVar13,(uint3)local_70);
    }
    else {
      local_70 = CONCAT13((char)(iVar8 / 3),(uint3)local_70) | 0xc0000000;
    }
    goto LAB_0041aa74;
  }
  if (DAT_00432ad8 == 0xbea) {
    iVar8 = 0;
    uVar4 = 0;
    puVar15 = (undefined4 *)(DAT_00432aa0 + 0x88);
    do {
      if (*(char *)(DAT_00432aa0 + 200 + iVar8) == '\0') {
        uVar4 = (uint)CONCAT11(0x80,(char)uVar4);
      }
      else {
        local_13d = 0;
        switch(*puVar15) {
        case 1:
          uVar3 = 1;
          break;
        case 2:
          uVar3 = 2;
          break;
        case 3:
          uVar3 = 3;
          break;
        case 4:
          uVar3 = 4;
          break;
        case 5:
          uVar3 = 5;
          break;
        case 7:
          uVar3 = 7;
          break;
        case 8:
          uVar3 = 8;
          break;
        case 9:
          uVar3 = 5;
          local_13d = 0x40;
          break;
        case 10:
          local_13d = 0x40;
        default:
          uVar3 = 6;
          break;
        case 0xb:
          uVar3 = 7;
          local_13d = 0x40;
          break;
        case 0xc:
          uVar3 = 8;
          local_13d = 0x40;
        }
        uVar4 = (uint)local_13d;
      }
      puVar15 = puVar15 + 1;
      local_134[iVar8 + 0xc0] = (byte)uVar3 | (byte)uVar4 | (byte)(uVar4 >> 8);
      iVar8 = iVar8 + 1;
    } while (iVar8 < 8);
    pcVar16 = Sleep_exref;
    goto LAB_0041aa74;
  }
  if (DAT_00432ad8 == 0x13ba) {
    iVar8 = 0;
    uVar4 = 0;
    puVar15 = (undefined4 *)(DAT_00432aa0 + 0x88);
    do {
      if (*(char *)(DAT_00432aa0 + 200 + iVar8) == '\0') {
        uVar4 = (uint)CONCAT11(0x80,(char)uVar4);
      }
      else {
        local_13d = 0;
        switch(*puVar15) {
        case 1:
        case 0xb:
          uVar3 = 1;
          break;
        case 2:
          uVar3 = 2;
          break;
        case 3:
          uVar3 = 3;
          break;
        case 4:
          uVar3 = 4;
          break;
        case 5:
          uVar3 = 5;
          break;
        case 7:
          uVar3 = 7;
          break;
        case 8:
          uVar3 = 8;
          break;
        case 9:
          uVar3 = 9;
          break;
        case 10:
          uVar3 = 10;
          break;
        case 0xc:
          local_13d = 0x40;
        default:
          uVar3 = 6;
          break;
        case 0xd:
          uVar3 = 7;
          local_13d = 0x40;
          break;
        case 0xe:
          uVar3 = 8;
          local_13d = 0x40;
          break;
        case 0xf:
          uVar3 = 9;
          local_13d = 0x40;
          break;
        case 0x10:
          uVar3 = 10;
          local_13d = 0x40;
          break;
        case 0x11:
          uVar3 = 0xb;
          local_13d = 0x40;
        }
        uVar4 = (uint)local_13d;
      }
      puVar15 = puVar15 + 1;
      local_134[iVar8 + 0xc0] = (byte)uVar3 | (byte)uVar4 | (byte)(uVar4 >> 8);
      iVar8 = iVar8 + 1;
    } while (iVar8 < 8);
    pcVar16 = Sleep_exref;
    goto LAB_0041aa74;
  }
  if (DAT_00432ad8 == 0xcff) {
    if (*(char *)(DAT_00432aa0 + 200) == '\0') {
      uVar10 = 0x8000;
    }
    else {
      uVar3 = *(uint *)(DAT_00432aa0 + 0x88);
      uVar10 = 0;
      if (0x3e < (int)uVar3) {
        uVar10 = 0x40;
        uVar3 = (int)uVar3 / 2 & 0xff;
      }
    }
    bVar1 = (byte)uVar10;
    bVar13 = (byte)uVar3 | bVar1;
    if (*(char *)(DAT_00432aa0 + 0xc9) == '\0') {
      bVar14 = 0x80;
    }
    else {
      uVar3 = *(uint *)(DAT_00432aa0 + 0x8c);
      bVar1 = 0;
      bVar14 = 0;
      if (0x3e < (int)uVar3) {
        bVar1 = 0x40;
        bVar14 = 0;
        uVar3 = (int)uVar3 / 2 & 0xff;
      }
    }
    local_74._0_2_ = CONCAT11((byte)uVar3 | bVar1 | bVar14,bVar13 | (byte)((ushort)uVar10 >> 8));
    if (*(char *)(DAT_00432aa0 + 0xca) == '\0') {
      bVar13 = 0x80;
    }
    else {
      uVar3 = *(uint *)(DAT_00432aa0 + 0x90);
      bVar1 = 0;
      bVar13 = 0;
      if (0x3e < (int)uVar3) {
        bVar1 = 0x40;
        bVar13 = 0;
        uVar3 = (int)uVar3 / 2 & 0xff;
      }
    }
    local_74._0_3_ = CONCAT12((byte)uVar3 | bVar1 | bVar13,(undefined2)local_74);
    if (*(char *)(DAT_00432aa0 + 0xcb) == '\0') {
      bVar13 = 0x80;
    }
    else {
      uVar3 = *(uint *)(DAT_00432aa0 + 0x94);
      bVar1 = 0;
      bVar13 = 0;
      if (0x3e < (int)uVar3) {
        bVar1 = 0x40;
        bVar13 = 0;
        uVar3 = (int)uVar3 / 2 & 0xff;
      }
    }
    local_74 = CONCAT13((byte)uVar3 | bVar1 | bVar13,(undefined3)local_74);
    if (*(char *)(DAT_00432aa0 + 0xcc) == '\0') {
      bVar13 = 0x80;
    }
    else {
      uVar3 = *(uint *)(DAT_00432aa0 + 0x98);
      bVar1 = 0;
      bVar13 = 0;
      if (0x3e < (int)uVar3) {
        bVar1 = 0x40;
        bVar13 = 0;
        uVar3 = (int)uVar3 / 2 & 0xff;
      }
    }
    bVar14 = (byte)uVar3 | bVar1;
    if (*(char *)(DAT_00432aa0 + 0xcd) == '\0') {
      bVar2 = 0x80;
    }
    else {
      uVar3 = *(uint *)(DAT_00432aa0 + 0x9c);
      bVar1 = 0;
      bVar2 = 0;
      if (0x3e < (int)uVar3) {
        bVar1 = 0x40;
        bVar2 = 0;
        uVar3 = (int)uVar3 / 2 & 0xff;
      }
    }
    local_70._0_2_ = CONCAT11((byte)uVar3 | bVar1 | bVar2,bVar14 | bVar13);
    if (*(char *)(DAT_00432aa0 + 0xce) == '\0') {
      bVar13 = 0x80;
    }
    else {
      uVar3 = *(uint *)(DAT_00432aa0 + 0xa0);
      bVar1 = 0;
      bVar13 = 0;
      if (0x3e < (int)uVar3) {
        bVar1 = 0x40;
        bVar13 = 0;
        uVar3 = (int)uVar3 / 2 & 0xff;
      }
    }
    local_70._0_3_ = CONCAT12((byte)uVar3 | bVar1 | bVar13,(undefined2)local_70);
    if (*(char *)(DAT_00432aa0 + 0xcf) == '\0') {
      local_70 = CONCAT13((byte)uVar3 | bVar1,(uint3)local_70) | 0x80000000;
      goto LAB_0041aa74;
    }
    uVar3 = *(uint *)(DAT_00432aa0 + 0xa4);
    bVar18 = SBORROW4(uVar3,0x3e);
    iVar8 = uVar3 - 0x3e;
    bVar17 = uVar3 == 0x3e;
LAB_0041a26b:
    bVar13 = 0;
    if (!bVar17 && bVar18 == iVar8 < 0) {
      bVar13 = 0x40;
      uVar3 = (int)uVar3 / 2 & 0xff;
    }
    local_70 = CONCAT13((byte)uVar3 | bVar13,(uint3)local_70);
    goto LAB_0041aa74;
  }
  if (DAT_00432ad8 == 0xd07) {
    iVar8 = *(int *)(DAT_00432aa0 + 0x88);
    iVar11 = iVar8 / 2;
    if (iVar8 < 0xa1) {
      iVar11 = iVar8;
    }
    iVar8 = *(int *)(DAT_00432aa0 + 0x8c);
    iVar7 = iVar8 / 2;
    if (iVar8 < 0xa1) {
      iVar7 = iVar8;
    }
    iVar8 = *(int *)(DAT_00432aa0 + 0x90);
    local_74._0_2_ = CONCAT11((&DAT_00425fc4)[iVar7 * 4],(&DAT_00425fc4)[iVar11 * 4]);
    iVar11 = iVar8 / 2;
    if (iVar8 < 0xa1) {
      iVar11 = iVar8;
    }
    iVar8 = *(int *)(DAT_00432aa0 + 0x94);
    local_74._0_3_ = CONCAT12((&DAT_00425fc4)[iVar11 * 4],(undefined2)local_74);
    iVar11 = iVar8 / 2;
    if (iVar8 < 0xa1) {
      iVar11 = iVar8;
    }
    iVar8 = *(int *)(DAT_00432aa0 + 0x98);
    local_74 = CONCAT13((&DAT_00425fc4)[iVar11 * 4],(undefined3)local_74);
    iVar11 = iVar8 / 2;
    if (iVar8 < 0xa1) {
      iVar11 = iVar8;
    }
    iVar8 = *(int *)(DAT_00432aa0 + 0x9c);
    iVar7 = iVar8 / 2;
    if (iVar8 < 0xa1) {
      iVar7 = iVar8;
    }
    iVar8 = *(int *)(DAT_00432aa0 + 0xa0);
    local_70._0_2_ = CONCAT11((&DAT_00425fc4)[iVar7 * 4],(&DAT_00425fc4)[iVar11 * 4]);
    iVar11 = iVar8 / 2;
    if (iVar8 < 0xa1) {
      iVar11 = iVar8;
    }
    iVar8 = *(int *)(DAT_00432aa0 + 0xa4);
    local_70._0_3_ = CONCAT12((&DAT_00425fc4)[iVar11 * 4],(undefined2)local_70);
    local_70 = (uint)(uint3)local_70;
    iVar11 = iVar8 / 2;
    if (iVar8 < 0xa1) {
      iVar11 = iVar8;
    }
    uVar3 = (uint)(byte)(&DAT_00425fc4)[iVar11 * 4];
    goto LAB_0041aa71;
  }
  if (DAT_00432ad8 == 0x24) {
    if (*(char *)(DAT_00432aa0 + 200) == '\0') {
      uVar10 = 0x8000;
    }
    else {
      uVar3 = *(int *)(DAT_00432aa0 + 0x88) - 1;
      uVar10 = 0;
      if (0x28 < (int)uVar3) {
        uVar10 = 0x40;
        uVar3 = (int)uVar3 / 2 & 0xff;
      }
    }
    bVar1 = (byte)uVar10;
    bVar13 = (byte)uVar3 | bVar1;
    if (*(char *)(DAT_00432aa0 + 0xc9) == '\0') {
      bVar14 = 0x80;
    }
    else {
      uVar3 = *(int *)(DAT_00432aa0 + 0x8c) - 1;
      bVar1 = 0;
      bVar14 = 0;
      if (0x28 < (int)uVar3) {
        bVar1 = 0x40;
        bVar14 = 0;
        uVar3 = (int)uVar3 / 2 & 0xff;
      }
    }
    local_74._0_2_ = CONCAT11((byte)uVar3 | bVar1 | bVar14,bVar13 | (byte)((ushort)uVar10 >> 8));
    if (*(char *)(DAT_00432aa0 + 0xca) == '\0') {
      bVar13 = 0x80;
    }
    else {
      uVar3 = *(int *)(DAT_00432aa0 + 0x90) - 1;
      bVar1 = 0;
      bVar13 = 0;
      if (0x28 < (int)uVar3) {
        bVar1 = 0x40;
        bVar13 = 0;
        uVar3 = (int)uVar3 / 2 & 0xff;
      }
    }
    local_74._0_3_ = CONCAT12((byte)uVar3 | bVar1 | bVar13,(undefined2)local_74);
    if (*(char *)(DAT_00432aa0 + 0xcb) == '\0') {
      bVar13 = 0x80;
    }
    else {
      uVar3 = *(int *)(DAT_00432aa0 + 0x94) - 1;
      bVar1 = 0;
      bVar13 = 0;
      if (0x28 < (int)uVar3) {
        bVar1 = 0x40;
        bVar13 = 0;
        uVar3 = (int)uVar3 / 2 & 0xff;
      }
    }
    local_74 = CONCAT13((byte)uVar3 | bVar1 | bVar13,(undefined3)local_74);
    if (*(char *)(DAT_00432aa0 + 0xcc) == '\0') {
      bVar13 = 0x80;
    }
    else {
      uVar3 = *(int *)(DAT_00432aa0 + 0x98) - 1;
      bVar1 = 0;
      bVar13 = 0;
      if (0x28 < (int)uVar3) {
        bVar1 = 0x40;
        bVar13 = 0;
        uVar3 = (int)uVar3 / 2 & 0xff;
      }
    }
    bVar14 = (byte)uVar3 | bVar1;
    if (*(char *)(DAT_00432aa0 + 0xcd) == '\0') {
      bVar2 = 0x80;
    }
    else {
      uVar3 = *(int *)(DAT_00432aa0 + 0x9c) - 1;
      bVar1 = 0;
      bVar2 = 0;
      if (0x28 < (int)uVar3) {
        bVar1 = 0x40;
        bVar2 = 0;
        uVar3 = (int)uVar3 / 2 & 0xff;
      }
    }
    local_70._0_2_ = CONCAT11((byte)uVar3 | bVar1 | bVar2,bVar14 | bVar13);
    if (*(char *)(DAT_00432aa0 + 0xce) == '\0') {
      bVar13 = 0x80;
    }
    else {
      uVar3 = *(int *)(DAT_00432aa0 + 0xa0) - 1;
      bVar1 = 0;
      bVar13 = 0;
      if (0x28 < (int)uVar3) {
        bVar1 = 0x40;
        bVar13 = 0;
        uVar3 = (int)uVar3 / 2 & 0xff;
      }
    }
    local_70._0_3_ = CONCAT12((byte)uVar3 | bVar1 | bVar13,(undefined2)local_70);
    if (*(char *)(DAT_00432aa0 + 0xcf) == '\0') {
      local_70 = CONCAT13((byte)uVar3 | bVar1,(uint3)local_70) | 0x80000000;
      goto LAB_0041aa74;
    }
    uVar3 = *(int *)(DAT_00432aa0 + 0xa4) - 1;
    bVar18 = SBORROW4(uVar3,0x28);
    iVar8 = *(int *)(DAT_00432aa0 + 0xa4) + -0x29;
    bVar17 = uVar3 == 0x28;
    goto LAB_0041a26b;
  }
  if (DAT_00432ad8 == 0x25) {
    bVar13 = 0;
    iVar8 = *(int *)(DAT_00432aa0 + 0x88);
    if (0x3c < iVar8) {
      bVar13 = 0x40;
      iVar8 = iVar8 / 2;
    }
    bVar1 = 0;
    iVar11 = *(int *)(DAT_00432aa0 + 0x8c);
    if (0x3c < iVar11) {
      bVar1 = 0x40;
      iVar11 = iVar11 / 2;
    }
    bVar14 = 0;
    local_74._0_2_ = CONCAT11((char)iVar11 - 1U | bVar1,(char)iVar8 - 1U | bVar13);
    iVar8 = *(int *)(DAT_00432aa0 + 0x90);
    if (0x3c < iVar8) {
      bVar14 = 0x40;
      iVar8 = iVar8 / 2;
    }
    bVar13 = 0;
    local_74._0_3_ = CONCAT12((char)iVar8 - 1U | bVar14,(undefined2)local_74);
    iVar8 = *(int *)(DAT_00432aa0 + 0x94);
    if (0x3c < iVar8) {
      bVar13 = 0x40;
      iVar8 = iVar8 / 2;
    }
    bVar1 = 0;
    local_74 = CONCAT13((char)iVar8 - 1U | bVar13,(undefined3)local_74);
    iVar8 = *(int *)(DAT_00432aa0 + 0x98);
    if (0x3c < iVar8) {
      bVar1 = 0x40;
      iVar8 = iVar8 / 2;
    }
    bVar13 = 0;
    iVar11 = *(int *)(DAT_00432aa0 + 0x9c);
    if (0x3c < iVar11) {
      bVar13 = 0x40;
      iVar11 = iVar11 / 2;
    }
    bVar14 = 0;
    local_70._0_2_ = CONCAT11((char)iVar11 - 1U | bVar13,(char)iVar8 - 1U | bVar1);
    iVar8 = *(int *)(DAT_00432aa0 + 0xa0);
    if (0x3c < iVar8) {
      bVar14 = 0x40;
      iVar8 = iVar8 / 2;
    }
    bVar13 = 0;
    local_70._0_3_ = CONCAT12((char)iVar8 - 1U | bVar14,(undefined2)local_70);
    local_70 = (uint)(uint3)local_70;
    iVar8 = *(int *)(DAT_00432aa0 + 0xa4);
    if (0x3c < iVar8) {
      bVar13 = 0x40;
      iVar8 = iVar8 / 2;
    }
    uVar3 = (uint)(byte)((char)iVar8 - 1U | bVar13);
    goto LAB_0041aa71;
  }
  if (DAT_00432ad8 == 0x26) {
    bVar13 = 0;
    iVar8 = *(int *)(DAT_00432aa0 + 0x88);
    if (0x50 < iVar8) {
      bVar13 = 0x80;
      iVar8 = iVar8 / 2;
    }
    bVar1 = 0;
    iVar11 = *(int *)(DAT_00432aa0 + 0x8c);
    if (0x50 < iVar11) {
      bVar1 = 0x80;
      iVar11 = iVar11 / 2;
    }
    bVar14 = 0;
    local_74._0_2_ = CONCAT11((char)iVar11 - 1U | bVar1,(char)iVar8 - 1U | bVar13);
    iVar8 = *(int *)(DAT_00432aa0 + 0x90);
    if (0x50 < iVar8) {
      bVar14 = 0x80;
      iVar8 = iVar8 / 2;
    }
    bVar13 = 0;
    local_74._0_3_ = CONCAT12((char)iVar8 - 1U | bVar14,(undefined2)local_74);
    iVar8 = *(int *)(DAT_00432aa0 + 0x94);
    if (0x50 < iVar8) {
      bVar13 = 0x80;
      iVar8 = iVar8 / 2;
    }
    bVar1 = 0;
    local_74 = CONCAT13((char)iVar8 - 1U | bVar13,(undefined3)local_74);
    iVar8 = *(int *)(DAT_00432aa0 + 0x98);
    if (0x50 < iVar8) {
      bVar1 = 0x80;
      iVar8 = iVar8 / 2;
    }
    bVar13 = 0;
    iVar11 = *(int *)(DAT_00432aa0 + 0x9c);
    if (0x50 < iVar11) {
      bVar13 = 0x80;
      iVar11 = iVar11 / 2;
    }
    bVar14 = 0;
    local_70._0_2_ = CONCAT11((char)iVar11 - 1U | bVar13,(char)iVar8 - 1U | bVar1);
    iVar8 = *(int *)(DAT_00432aa0 + 0xa0);
    if (0x50 < iVar8) {
      bVar14 = 0x80;
      iVar8 = iVar8 / 2;
    }
    local_70._0_3_ = CONCAT12((char)iVar8 - 1U | bVar14,(undefined2)local_70);
    iVar8 = *(int *)(DAT_00432aa0 + 0xa4);
    bVar18 = SBORROW4(iVar8,0x50);
    iVar11 = iVar8 + -0x50;
    bVar17 = iVar8 == 0x50;
LAB_0041a444:
    local_70 = (uint)(uint3)local_70;
    bVar13 = 0;
    if (!bVar17 && bVar18 == iVar11 < 0) {
      bVar13 = 0x80;
      iVar8 = iVar8 / 2;
    }
    uVar3 = (uint)(byte)((char)iVar8 - 1U | bVar13);
  }
  else {
    if (DAT_00432ad8 == 0x3c) {
      bVar13 = 0;
      iVar8 = *(int *)(DAT_00432aa0 + 0x88);
      if (0x78 < iVar8) {
        bVar13 = 0x80;
        iVar8 = iVar8 / 2;
      }
      bVar1 = 0;
      iVar11 = *(int *)(DAT_00432aa0 + 0x8c);
      if (0x78 < iVar11) {
        bVar1 = 0x80;
        iVar11 = iVar11 / 2;
      }
      bVar14 = 0;
      local_74._0_2_ = CONCAT11((char)iVar11 - 1U | bVar1,(char)iVar8 - 1U | bVar13);
      iVar8 = *(int *)(DAT_00432aa0 + 0x90);
      if (0x78 < iVar8) {
        bVar14 = 0x80;
        iVar8 = iVar8 / 2;
      }
      bVar13 = 0;
      local_74._0_3_ = CONCAT12((char)iVar8 - 1U | bVar14,(undefined2)local_74);
      iVar8 = *(int *)(DAT_00432aa0 + 0x94);
      if (0x78 < iVar8) {
        bVar13 = 0x80;
        iVar8 = iVar8 / 2;
      }
      bVar1 = 0;
      local_74 = CONCAT13((char)iVar8 - 1U | bVar13,(undefined3)local_74);
      iVar8 = *(int *)(DAT_00432aa0 + 0x98);
      if (0x78 < iVar8) {
        bVar1 = 0x80;
        iVar8 = iVar8 / 2;
      }
      bVar13 = 0;
      iVar11 = *(int *)(DAT_00432aa0 + 0x9c);
      if (0x78 < iVar11) {
        bVar13 = 0x80;
        iVar11 = iVar11 / 2;
      }
      bVar14 = 0;
      local_70._0_2_ = CONCAT11((char)iVar11 - 1U | bVar13,(char)iVar8 - 1U | bVar1);
      iVar8 = *(int *)(DAT_00432aa0 + 0xa0);
      if (0x78 < iVar8) {
        bVar14 = 0x80;
        iVar8 = iVar8 / 2;
      }
      local_70._0_3_ = CONCAT12((char)iVar8 - 1U | bVar14,(undefined2)local_70);
      iVar8 = *(int *)(DAT_00432aa0 + 0xa4);
      bVar18 = SBORROW4(iVar8,0x78);
      iVar11 = iVar8 + -0x78;
      bVar17 = iVar11 == 0;
      goto LAB_0041a444;
    }
    if (DAT_00432ad8 == 0x1900) {
      bVar13 = 0;
      iVar8 = *(int *)(DAT_00432aa0 + 0x88);
      if (0x7c < iVar8) {
        bVar13 = 0x80;
        iVar8 = iVar8 / 2;
      }
      bVar1 = 0;
      iVar11 = *(int *)(DAT_00432aa0 + 0x8c);
      if (0x7c < iVar11) {
        bVar1 = 0x80;
        iVar11 = iVar11 / 2;
      }
      bVar14 = 0;
      local_74._0_2_ = CONCAT11((char)iVar11 - 2U | bVar1,(char)iVar8 - 2U | bVar13);
      iVar8 = *(int *)(DAT_00432aa0 + 0x90);
      if (0x7c < iVar8) {
        bVar14 = 0x80;
        iVar8 = iVar8 / 2;
      }
      bVar13 = 0;
      local_74._0_3_ = CONCAT12((char)iVar8 - 2U | bVar14,(undefined2)local_74);
      iVar8 = *(int *)(DAT_00432aa0 + 0x94);
      if (0x7c < iVar8) {
        bVar13 = 0x80;
        iVar8 = iVar8 / 2;
      }
      bVar1 = 0;
      local_74 = CONCAT13((char)iVar8 - 2U | bVar13,(undefined3)local_74);
      iVar8 = *(int *)(DAT_00432aa0 + 0x98);
      if (0x7c < iVar8) {
        bVar1 = 0x80;
        iVar8 = iVar8 / 2;
      }
      bVar13 = 0;
      iVar11 = *(int *)(DAT_00432aa0 + 0x9c);
      if (0x7c < iVar11) {
        bVar13 = 0x80;
        iVar11 = iVar11 / 2;
      }
      bVar14 = 0;
      local_70._0_2_ = CONCAT11((char)iVar11 - 2U | bVar13,(char)iVar8 - 2U | bVar1);
      iVar8 = *(int *)(DAT_00432aa0 + 0xa0);
      if (0x7c < iVar8) {
        bVar14 = 0x80;
        iVar8 = iVar8 / 2;
      }
      bVar13 = 0;
      local_70._0_3_ = CONCAT12((char)iVar8 - 2U | bVar14,(undefined2)local_70);
      local_70 = (uint)(uint3)local_70;
      iVar8 = *(int *)(DAT_00432aa0 + 0xa4);
      if (0x7c < iVar8) {
        bVar13 = 0x80;
        iVar8 = iVar8 / 2;
      }
      uVar3 = (uint)(byte)((char)iVar8 - 2U | bVar13);
      goto LAB_0041aa71;
    }
    if (DAT_00432ad8 == 0xc20) {
      iVar8 = *(int *)(DAT_00432aa0 + 0x88);
      bVar13 = (byte)(iVar8 / 2);
      if (iVar8 < 0x6b) {
        bVar13 = (byte)iVar8;
      }
      iVar11 = *(int *)(DAT_00432aa0 + 0x8c);
      bVar1 = (byte)(iVar11 / 2);
      if (iVar11 < 0x6b) {
        bVar1 = (byte)iVar11;
      }
      iVar7 = *(int *)(DAT_00432aa0 + 0x90);
      local_74._0_2_ =
           CONCAT11(bVar1 | (iVar11 < 0x6b) - 1U & 0x80,bVar13 | (iVar8 < 0x6b) - 1U & 0x80);
      bVar13 = (byte)(iVar7 / 2);
      if (iVar7 < 0x6b) {
        bVar13 = (byte)iVar7;
      }
      iVar8 = *(int *)(DAT_00432aa0 + 0x94);
      local_74._0_3_ = CONCAT12(bVar13 | (iVar7 < 0x6b) - 1U & 0x80,(undefined2)local_74);
      iVar11 = *(int *)(DAT_00432aa0 + 0x98);
      bVar13 = (byte)(iVar8 / 2);
      if (iVar8 < 0x6b) {
        bVar13 = (byte)iVar8;
      }
      local_74 = CONCAT13(bVar13 | (iVar8 < 0x6b) - 1U & 0x80,(undefined3)local_74);
      iVar8 = *(int *)(DAT_00432aa0 + 0x9c);
      bVar13 = (byte)(iVar11 / 2);
      if (iVar11 < 0x6b) {
        bVar13 = (byte)iVar11;
      }
      bVar1 = (byte)(iVar8 / 2);
      if (iVar8 < 0x6b) {
        bVar1 = (byte)iVar8;
      }
      iVar7 = *(int *)(DAT_00432aa0 + 0xa0);
      local_70._0_2_ =
           CONCAT11(bVar1 | (iVar8 < 0x6b) - 1U & 0x80,bVar13 | (iVar11 < 0x6b) - 1U & 0x80);
      iVar8 = *(int *)(DAT_00432aa0 + 0xa4);
      bVar13 = (byte)(iVar7 / 2);
      if (iVar7 < 0x6b) {
        bVar13 = (byte)iVar7;
      }
      local_70._0_3_ = CONCAT12(bVar13 | (iVar7 < 0x6b) - 1U & 0x80,(undefined2)local_70);
      bVar13 = (byte)(iVar8 / 2);
      if (iVar8 < 0x6b) {
        bVar13 = (byte)iVar8;
      }
      local_70 = CONCAT13(bVar13 | (iVar8 < 0x6b) - 1U & 0x80,(uint3)local_70);
      goto LAB_0041aa74;
    }
    if (DAT_00432ad8 == 0xd02) {
      local_74._0_2_ =
           CONCAT11(*(char *)(DAT_00432aa0 + 0x8c) + -1,*(char *)(DAT_00432aa0 + 0x88) + -1);
      local_74._0_3_ = CONCAT12(*(char *)(DAT_00432aa0 + 0x90) + -1,(undefined2)local_74);
      local_74 = CONCAT13(*(char *)(DAT_00432aa0 + 0x94) + -1,(undefined3)local_74);
      local_70._0_2_ =
           CONCAT11(*(char *)(DAT_00432aa0 + 0x9c) + -1,*(char *)(DAT_00432aa0 + 0x98) + -1);
      local_70._0_3_ = CONCAT12(*(char *)(DAT_00432aa0 + 0xa0) + -1,(undefined2)local_70);
      local_70 = (uint)(uint3)local_70;
      uVar3 = (uint)(byte)(*(char *)(DAT_00432aa0 + 0xa4) - 1);
    }
    else if (DAT_00432ad8 == 0xd05) {
      uVar3 = *(uint *)(DAT_00432aa0 + 0x88);
      if (0x50 < (int)uVar3) {
        uVar3 = (uint)(byte)((byte)((int)uVar3 / 2) | 0x80);
      }
      uVar4 = *(uint *)(DAT_00432aa0 + 0x8c);
      if (0x50 < (int)uVar4) {
        uVar4 = (uint)(byte)((byte)((int)uVar4 / 2) | 0x80);
      }
      uVar5 = *(uint *)(DAT_00432aa0 + 0x90);
      if (0x50 < (int)uVar5) {
        uVar5 = (uint)(byte)((byte)((int)uVar5 / 2) | 0x80);
      }
      uVar6 = *(uint *)(DAT_00432aa0 + 0x94);
      if (0x50 < (int)uVar6) {
        uVar6 = (uint)(byte)((byte)((int)uVar6 / 2) | 0x80);
      }
      local_74 = CONCAT13((char)uVar6,CONCAT12((char)uVar5,CONCAT11((char)uVar4,(char)uVar3)));
      uVar3 = *(uint *)(DAT_00432aa0 + 0x98);
      if (0x50 < (int)uVar3) {
        uVar3 = (uint)(byte)((byte)((int)uVar3 / 2) | 0x80);
      }
      uVar4 = *(uint *)(DAT_00432aa0 + 0x9c);
      if (0x50 < (int)uVar4) {
        uVar4 = (uint)(byte)((byte)((int)uVar4 / 2) | 0x80);
      }
      uVar5 = *(uint *)(DAT_00432aa0 + 0xa0);
      if (0x50 < (int)uVar5) {
        uVar5 = (uint)(byte)((byte)((int)uVar5 / 2) | 0x80);
      }
      local_70 = (uint)CONCAT12((char)uVar5,CONCAT11((char)uVar4,(char)uVar3));
      uVar3 = *(uint *)(DAT_00432aa0 + 0xa4);
      if (0x50 < (int)uVar3) {
        uVar3 = (uint)(byte)((byte)((int)uVar3 / 2) | 0x80);
      }
    }
    else if (DAT_00432ad8 == 0xd2a) {
      iVar8 = *(int *)(DAT_00432aa0 + 0x88);
      if (iVar8 < 0xc9) {
        if (0 < iVar8) {
          cVar9 = (char)iVar8 + -1;
          goto LAB_0041a8b1;
        }
      }
      else {
        cVar9 = (char)iVar8 + -0x65;
LAB_0041a8b1:
        local_74 = CONCAT31(local_74._1_3_,cVar9);
      }
      iVar8 = *(int *)(DAT_00432aa0 + 0x8c);
      if (iVar8 < 0xc9) {
        if (0 < iVar8) {
          cVar9 = (char)iVar8 + -1;
          goto LAB_0041a8cb;
        }
      }
      else {
        cVar9 = (char)iVar8 + -0x65;
LAB_0041a8cb:
        local_74._0_2_ = CONCAT11(cVar9,(undefined1)local_74);
      }
      iVar8 = *(int *)(DAT_00432aa0 + 0x90);
      if (iVar8 < 0xc9) {
        if (0 < iVar8) {
          cVar9 = (char)iVar8 + -1;
          goto LAB_0041a8e5;
        }
      }
      else {
        cVar9 = (char)iVar8 + -0x65;
LAB_0041a8e5:
        local_74._0_3_ = CONCAT12(cVar9,(undefined2)local_74);
      }
      iVar8 = *(int *)(DAT_00432aa0 + 0x94);
      if (iVar8 < 0xc9) {
        if (0 < iVar8) {
          cVar9 = (char)iVar8 + -1;
          goto LAB_0041a8ff;
        }
      }
      else {
        cVar9 = (char)iVar8 + -0x65;
LAB_0041a8ff:
        local_74 = CONCAT13(cVar9,(undefined3)local_74);
      }
      iVar8 = *(int *)(DAT_00432aa0 + 0x98);
      if (iVar8 < 0xc9) {
        if (0 < iVar8) {
          cVar9 = (char)iVar8 + -1;
          goto LAB_0041a919;
        }
      }
      else {
        cVar9 = (char)iVar8 + -0x65;
LAB_0041a919:
        local_70 = CONCAT31(local_70._1_3_,cVar9);
      }
      iVar8 = *(int *)(DAT_00432aa0 + 0x9c);
      if (iVar8 < 0xc9) {
        if (0 < iVar8) {
          cVar9 = (char)iVar8 + -1;
          goto LAB_0041a933;
        }
      }
      else {
        cVar9 = (char)iVar8 + -0x65;
LAB_0041a933:
        local_70._0_2_ = CONCAT11(cVar9,(undefined1)local_70);
      }
      iVar8 = *(int *)(DAT_00432aa0 + 0xa0);
      if (iVar8 < 0xc9) {
        if (0 < iVar8) {
          cVar9 = (char)iVar8 + -1;
          goto LAB_0041a94d;
        }
      }
      else {
        cVar9 = (char)iVar8 + -0x65;
LAB_0041a94d:
        local_70._0_3_ = CONCAT12(cVar9,(undefined2)local_70);
      }
      iVar8 = *(int *)(DAT_00432aa0 + 0xa4);
      if (iVar8 < 0xc9) {
        if (iVar8 < 1) goto LAB_0041aa74;
        uVar3 = (uint)(byte)((char)iVar8 - 1);
      }
      else {
        uVar3 = (uint)(byte)((char)iVar8 + 0x9b);
      }
    }
    else {
      if (DAT_00432ad8 != 0xcef) goto LAB_0041aa74;
      iVar8 = *(int *)(DAT_00432aa0 + 0x88);
      iVar11 = iVar8 / 2;
      if (iVar8 < 0x79) {
        iVar11 = iVar8;
      }
      iVar8 = *(int *)(DAT_00432aa0 + 0x8c);
      iVar7 = iVar8 / 2;
      if (iVar8 < 0x79) {
        iVar7 = iVar8;
      }
      iVar8 = *(int *)(DAT_00432aa0 + 0x90);
      local_74._0_2_ = CONCAT11((&DAT_00425de4)[iVar7 * 4],(&DAT_00425de4)[iVar11 * 4]);
      iVar11 = iVar8 / 2;
      if (iVar8 < 0x79) {
        iVar11 = iVar8;
      }
      iVar8 = *(int *)(DAT_00432aa0 + 0x94);
      local_74._0_3_ = CONCAT12((&DAT_00425de4)[iVar11 * 4],(undefined2)local_74);
      iVar11 = iVar8 / 2;
      if (iVar8 < 0x79) {
        iVar11 = iVar8;
      }
      iVar8 = *(int *)(DAT_00432aa0 + 0x98);
      local_74 = CONCAT13((&DAT_00425de4)[iVar11 * 4],(undefined3)local_74);
      iVar11 = iVar8 / 2;
      if (iVar8 < 0x79) {
        iVar11 = iVar8;
      }
      iVar8 = *(int *)(DAT_00432aa0 + 0x9c);
      iVar7 = iVar8 / 2;
      if (iVar8 < 0x79) {
        iVar7 = iVar8;
      }
      iVar8 = *(int *)(DAT_00432aa0 + 0xa0);
      local_70._0_2_ = CONCAT11((&DAT_00425de4)[iVar7 * 4],(&DAT_00425de4)[iVar11 * 4]);
      iVar11 = iVar8 / 2;
      if (iVar8 < 0x79) {
        iVar11 = iVar8;
      }
      iVar8 = *(int *)(DAT_00432aa0 + 0xa4);
      local_70._0_3_ = CONCAT12((&DAT_00425de4)[iVar11 * 4],(undefined2)local_70);
      local_70 = (uint)(uint3)local_70;
      iVar11 = iVar8 / 2;
      if (iVar8 < 0x79) {
        iVar11 = iVar8;
      }
      uVar3 = (uint)(byte)(&DAT_00425de4)[iVar11 * 4];
    }
  }
LAB_0041aa71:
  local_70 = CONCAT13((char)uVar3,(uint3)local_70);
LAB_0041aa74:
  memset(local_134,0,0xc0);
  local_13c = local_74;
  local_138 = local_70;
  iVar8 = (**(code **)(param_1 + 0x798))(&local_13c,0x20);
  if (iVar8 != 0) {
    (*pcVar16)(10);
  }
  return iVar8;
}


