// Program: SM809 mouse Software.exe
// Function: FUN_0041ab50
// Entry: 0041ab50
// Body: 0041ab50 - 0041b6e9
// Signature: undefined4 FUN_0041ab50(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

undefined4 __fastcall FUN_0041ab50(int param_1)

{
  code *pcVar1;
  byte bVar2;
  char cVar3;
  undefined1 *puVar4;
  uint uVar5;
  int iVar6;
  undefined4 uVar7;
  undefined1 uVar9;
  ushort uVar8;
  undefined1 uVar12;
  undefined2 uVar10;
  undefined3 uVar13;
  uint uVar11;
  char cVar14;
  int iVar15;
  int iVar16;
  uint uVar17;
  byte *pbVar18;
  int iVar19;
  undefined4 *puVar20;
  uint *puVar21;
  int local_6e8;
  int local_6e4;
  int local_6e0;
  int local_6d4;
  undefined4 local_6d0 [320];
  undefined4 local_1d0;
  undefined4 auStack_1cc [63];
  undefined4 local_d0;
  undefined4 uStack_cc;
  undefined4 uStack_c8;
  undefined4 uStack_c4;
  undefined4 local_c0;
  undefined4 uStack_bc;
  undefined4 uStack_b8;
  undefined4 uStack_b4;
  undefined1 local_b0 [40];
  byte local_88;
  undefined1 uStack_87;
  undefined2 local_86;
  undefined1 auStack_84 [2];
  undefined2 uStack_82;
  undefined1 auStack_80 [120];
  undefined4 local_8;
  
  local_8 = DAT_00432008 ^ (uint)(auStack_80 + 0x7c);
  local_6e8 = 1;
  cVar3 = '\0';
  memset(&local_1d0,0,0x100);
  memset(local_6d0,0,0x500);
  iVar16 = DAT_00432aa0;
  local_6e4 = 0;
  do {
    bVar2 = *(byte *)(local_6e4 * 0x72c + 0x219 + iVar16);
    iVar15 = local_6e4 * 0x72c + iVar16;
    memset(&local_88,0,0x80);
    puVar4 = &DAT_0042511c;
    uVar11 = (uint)local_86;
    uVar17 = (uint)CONCAT11(local_88,uStack_87);
    do {
      if (*(uint *)(puVar4 + -4) == (uint)bVar2) {
        uVar17 = (uint)CONCAT11(*puVar4,puVar4[4]);
        uVar11 = (uint)CONCAT11(puVar4[0xc],puVar4[8]);
        local_86 = (ushort)(byte)puVar4[8];
      }
      uVar10 = (undefined2)uVar17;
      puVar4 = puVar4 + 0x14;
    } while ((int)puVar4 < 0x4255e0);
    uVar9 = (undefined1)(uVar11 >> 8);
    local_86 = CONCAT11(uVar9,(undefined1)local_86);
    uVar12 = (undefined1)(uVar17 >> 8);
    _local_88 = CONCAT11((char)uVar17,uVar12);
    uVar13 = (undefined3)(uVar17 >> 8);
    if (bVar2 == 0x15) {
      uVar10 = (undefined2)CONCAT31(uVar13,*(undefined1 *)(iVar15 + 0x22c));
      uVar11 = CONCAT31((int3)(uVar11 >> 8),*(undefined1 *)(iVar15 + 0x22d));
      _local_88 = CONCAT11(*(undefined1 *)(iVar15 + 0x22c),uVar12);
      local_86 = CONCAT11(uVar9,*(undefined1 *)(iVar15 + 0x22d));
LAB_0041aca6:
      uVar8 = (ushort)uVar11;
      if (((char)((ushort)uVar10 >> 8) == '\t') && (local_6e8 < 0xc)) {
        uVar8 = (ushort)CONCAT31((int3)(uVar11 >> 8),(char)local_6e8);
        local_6e8 = local_6e8 + 1;
        goto LAB_0041ace8;
      }
    }
    else {
      if (bVar2 == 10) {
        uVar10 = (undefined2)CONCAT31(uVar13,0xf0);
        uVar11 = (uint)CONCAT11(*(undefined1 *)(iVar15 + 0x82c),*(undefined1 *)(iVar15 + 0x830));
        _local_88 = CONCAT11(0xf0,uVar12);
        local_86 = CONCAT11(*(undefined1 *)(iVar15 + 0x82c),*(undefined1 *)(iVar15 + 0x830));
        goto LAB_0041aca6;
      }
      if (bVar2 == 0x16) {
        uVar10 = (undefined2)CONCAT31(uVar13,*(undefined1 *)(iVar15 + 0x224));
        _local_88 = CONCAT11(*(undefined1 *)(iVar15 + 0x224),uVar12);
        goto LAB_0041aca6;
      }
      if ((bVar2 != 0x79) && (bVar2 != 0x39)) goto LAB_0041aca6;
      _local_88 = 8;
      local_86 = 0;
      uVar8 = (ushort)(byte)(cVar3 + 4);
      uVar10 = 0x800;
      cVar3 = cVar3 + '\x01';
LAB_0041ace8:
      local_86 = CONCAT11(local_86._1_1_,(char)uVar8);
    }
    iVar19 = param_1 + local_6e4 * 5;
    if (*(char *)(iVar19 + 0x158c) == '\x01') {
      *(char *)(local_6d0 + local_6e4 + 0x140) = (char)((ushort)uVar10 >> 8);
      *(char *)((int)local_6d0 + local_6e4 * 4 + 0x501) = (char)uVar10;
      *(char *)((int)auStack_1cc + local_6e4 * 4 + -2) = (char)uVar8;
      *(char *)((int)auStack_1cc + local_6e4 * 4 + -1) = (char)(uVar8 >> 8);
    }
    else {
      *(undefined1 *)(local_6d0 + local_6e4 + 0x140) = *(undefined1 *)(iVar19 + 0x1588);
      *(undefined1 *)((int)local_6d0 + local_6e4 * 4 + 0x501) = *(undefined1 *)(iVar19 + 0x1589);
      *(undefined1 *)((int)auStack_1cc + local_6e4 * 4 + -2) = *(undefined1 *)(iVar19 + 0x158a);
      *(undefined1 *)((int)auStack_1cc + local_6e4 * 4 + -1) =
           *(undefined1 *)(local_6e4 * 5 + 0x158b + param_1);
    }
    memset(&local_88,0,0x80);
    if (bVar2 == 0x16) {
      uVar11 = (uint)*(ushort *)(iVar15 + 0x232);
      if (uVar11 != 0) {
        uVar17 = 2;
        _local_88 = CONCAT11((char)*(undefined4 *)(iVar15 + 0x234),
                             (char)((uint)*(undefined4 *)(iVar15 + 0x234) >> 8));
        local_6d4 = 0;
        if (uVar11 != 0) {
          puVar20 = (undefined4 *)(iVar15 + 0x5b4);
          do {
            uVar5 = (uint)*(ushort *)(puVar20 + -1);
            cVar14 = *(char *)((int)puVar20 + -6);
            if (*(ushort *)(puVar20 + -1) < 0x4f7) {
              bVar2 = (byte)(uVar5 / 10);
              if (cVar14 == '\0') {
                uVar7 = *puVar20;
                auStack_84[uVar17 - 1] = (char)((uint)uVar7 >> 8);
                auStack_84[uVar17 - 2] = (char)uVar7;
                uVar7 = puVar20[1];
                auStack_84[uVar17 + 1] = (char)((uint)uVar7 >> 8);
                iVar15 = 6;
                local_b0[uVar17 + 0x29] = 0xfb;
                auStack_84[uVar17] = (char)uVar7;
              }
              else {
                if (cVar14 == '\x01') {
                  bVar2 = bVar2 | 1;
                }
                else if (cVar14 == '\x02') {
                  bVar2 = bVar2 | 0x81;
                }
                local_b0[uVar17 + 0x29] = *(undefined1 *)((int)puVar20 + -7);
                iVar15 = 2;
              }
              local_b0[uVar17 + 0x28] = bVar2;
            }
            else {
              bVar2 = (byte)((uVar5 % 0x14 + 5) / 10);
              uVar12 = (undefined1)(uVar5 / 0x14);
              uVar9 = (undefined1)(uVar5 / 0x14 >> 8);
              if (cVar14 == '\0') {
                if (0x7f < uVar17) {
LAB_0041b6e4:
                  FUN_004203a0();
                  pcVar1 = (code *)swi(3);
                  uVar7 = (*pcVar1)();
                  return uVar7;
                }
                uVar7 = *puVar20;
                *(undefined2 *)(local_b0 + uVar17 + 0x28) = 0xfb00;
                auStack_84[uVar17 - 1] = (char)((uint)uVar7 >> 8);
                auStack_84[uVar17 - 2] = (char)uVar7;
                uVar7 = puVar20[1];
                auStack_84[uVar17 + 1] = (char)((uint)uVar7 >> 8);
                auStack_84[uVar17] = (char)uVar7;
                if (0x7f < uVar17 + 6) goto LAB_0041b6e4;
                auStack_84[uVar17 + 2] = 0;
                auStack_80[uVar17] = uVar9;
                iVar15 = 10;
                auStack_80[uVar17 - 1] = 1;
                auStack_80[uVar17 + 1] = uVar12;
              }
              else {
                if (cVar14 == '\x01') {
LAB_0041aeab:
                  local_b0[uVar17 + 0x28] = bVar2;
                  local_b0[uVar17 + 0x29] = *(undefined1 *)((int)puVar20 + -7);
                }
                else if (cVar14 == '\x02') {
                  bVar2 = bVar2 | 0x80;
                  goto LAB_0041aeab;
                }
                if (0x7f < uVar17 + 2) goto LAB_0041b6e4;
                auStack_84[uVar17 - 2] = 0;
                auStack_84[uVar17] = uVar9;
                iVar15 = 6;
                auStack_84[uVar17 - 1] = 1;
                auStack_84[uVar17 + 1] = uVar12;
              }
            }
            puVar20 = puVar20 + 4;
            local_6d4 = local_6d4 + 1;
            uVar17 = uVar17 + iVar15;
          } while (local_6d4 < (int)uVar11);
        }
      }
      pbVar18 = &local_88;
      puVar20 = local_6d0 + (local_6e8 + -2) * 0x20;
      for (iVar15 = 0x20; iVar15 != 0; iVar15 = iVar15 + -1) {
        *puVar20 = *(undefined4 *)pbVar18;
        pbVar18 = pbVar18 + 4;
        puVar20 = puVar20 + 1;
      }
    }
    else if (bVar2 == 0x39) {
      uVar11 = (uint)*(ushort *)(iVar15 + 0x232);
      if (uVar11 != 0) {
        uVar17 = 2;
        _local_88 = CONCAT11((char)*(undefined4 *)(iVar15 + 0x234),
                             (char)((uint)*(undefined4 *)(iVar15 + 0x234) >> 8));
        local_6e0 = 0;
        if (uVar11 != 0) {
          puVar20 = (undefined4 *)(iVar15 + 0x5b4);
          do {
            uVar5 = (uint)*(ushort *)(puVar20 + -1);
            cVar14 = *(char *)((int)puVar20 + -6);
            if (*(ushort *)(puVar20 + -1) < 0x4f7) {
              bVar2 = (byte)(uVar5 / 10);
              if (cVar14 == '\0') {
                local_b0[uVar17 + 0x28] = bVar2;
                uVar7 = *puVar20;
                auStack_84[uVar17 - 1] = (char)((uint)uVar7 >> 8);
                auStack_84[uVar17 - 2] = (char)uVar7;
                uVar7 = puVar20[1];
                auStack_84[uVar17 + 1] = (char)((uint)uVar7 >> 8);
                iVar15 = 6;
                local_b0[uVar17 + 0x29] = 0xfb;
                auStack_84[uVar17] = (char)uVar7;
              }
              else {
                if (cVar14 == '\x01') {
                  bVar2 = bVar2 | 1;
                }
                else if (cVar14 == '\x02') {
                  bVar2 = bVar2 | 0x81;
                }
                local_b0[uVar17 + 0x29] = *(undefined1 *)((int)puVar20 + -7);
                iVar15 = 2;
                local_b0[uVar17 + 0x28] = bVar2;
              }
            }
            else {
              bVar2 = (byte)((uVar5 % 0x14 + 5) / 10);
              uVar12 = (undefined1)(uVar5 / 0x14);
              uVar9 = (undefined1)(uVar5 / 0x14 >> 8);
              if (cVar14 == '\0') {
                if (0x7f < uVar17) goto LAB_0041b6e4;
                uVar7 = *puVar20;
                *(undefined2 *)(local_b0 + uVar17 + 0x28) = 0xfb00;
                auStack_84[uVar17 - 1] = (char)((uint)uVar7 >> 8);
                auStack_84[uVar17 - 2] = (char)uVar7;
                uVar7 = puVar20[1];
                auStack_84[uVar17 + 1] = (char)((uint)uVar7 >> 8);
                auStack_84[uVar17] = (char)uVar7;
                if (0x7f < uVar17 + 6) goto LAB_0041b6e4;
                auStack_84[uVar17 + 2] = 0;
                auStack_80[uVar17] = uVar9;
                iVar15 = 10;
                auStack_80[uVar17 - 1] = 1;
                auStack_80[uVar17 + 1] = uVar12;
              }
              else {
                if (cVar14 == '\x01') {
LAB_0041b0be:
                  local_b0[uVar17 + 0x28] = bVar2;
                  local_b0[uVar17 + 0x29] = *(undefined1 *)((int)puVar20 + -7);
                }
                else if (cVar14 == '\x02') {
                  bVar2 = bVar2 | 0x80;
                  goto LAB_0041b0be;
                }
                if (0x7f < uVar17 + 2) goto LAB_0041b6e4;
                auStack_84[uVar17 - 2] = 0;
                auStack_84[uVar17] = uVar9;
                iVar15 = 6;
                auStack_84[uVar17 - 1] = 1;
                auStack_84[uVar17 + 1] = uVar12;
              }
            }
            puVar20 = puVar20 + 4;
            local_6e0 = local_6e0 + 1;
            uVar17 = uVar17 + iVar15;
          } while (local_6e0 < (int)uVar11);
        }
      }
    }
    else if (bVar2 == 0x79) {
      uVar11 = (uint)*(ushort *)(iVar15 + 0x232);
      if (uVar11 == 0) {
        _local_88 = CONCAT11(1,local_88);
      }
      else {
        iVar19 = 2;
        _local_88 = CONCAT11((char)*(undefined4 *)(iVar15 + 0x234),
                             (char)((uint)*(undefined4 *)(iVar15 + 0x234) >> 8));
        local_6d4 = 0;
        if (uVar11 < 0x10) {
          if (uVar11 != 0) {
            puVar21 = (uint *)(iVar15 + 0x444);
            do {
              uVar17 = puVar21[-1];
              bVar2 = (byte)(*(ushort *)((int)puVar21 + 6) / 10);
              if ((uVar17 == 0) && (*puVar21 == 0)) {
                *(undefined2 *)(local_b0 + iVar19 + 0x29) = 0x81f0;
                local_b0[iVar19 + 0x28] = bVar2 | 1;
                iVar15 = 4;
                auStack_84[iVar19 + -1] = 0xf0;
              }
              else {
                local_b0[iVar19 + 0x29] = 0xf0;
                local_b0[iVar19 + 0x28] = bVar2 | 1;
                if (0x7f < iVar19 + 2U) goto LAB_0041b6e4;
                auStack_84[iVar19 + -2] = 0;
                auStack_84[iVar19 + -1] = 0xfa;
                if ((int)uVar17 < 0) {
                  bVar2 = (byte)((int)uVar17 >> 0x1f);
                  uVar17 = (uint)(byte)-(((byte)uVar17 ^ bVar2) - bVar2);
                }
                auStack_84[iVar19] = (char)uVar17;
                uVar17 = *puVar21;
                if ((int)uVar17 < 0) {
                  bVar2 = (byte)((int)uVar17 >> 0x1f);
                  uVar17 = (uint)(byte)-(((byte)uVar17 ^ bVar2) - bVar2);
                }
                auStack_84[iVar19 + 1] = (char)uVar17;
                iVar15 = 8;
                *(undefined2 *)(auStack_84 + iVar19 + 2) = 0xf081;
              }
              puVar21 = puVar21 + 3;
              local_6d4 = local_6d4 + 1;
              iVar19 = iVar19 + iVar15;
            } while (local_6d4 < (int)uVar11);
          }
        }
        else {
          puVar21 = (uint *)(iVar15 + 0x444);
          do {
            uVar17 = puVar21[-1];
            bVar2 = (byte)(*(ushort *)((int)puVar21 + 6) / 10);
            if ((uVar17 == 0) && (*puVar21 == 0)) {
              *(undefined2 *)(local_b0 + iVar19 + 0x29) = 0x81f0;
              local_b0[iVar19 + 0x28] = bVar2 | 1;
              iVar6 = 4;
              auStack_84[iVar19 + -1] = 0xf0;
            }
            else {
              local_b0[iVar19 + 0x29] = 0xf0;
              local_b0[iVar19 + 0x28] = bVar2 | 1;
              if (0x7f < iVar19 + 2U) goto LAB_0041b6e4;
              auStack_84[iVar19 + -2] = 0;
              auStack_84[iVar19 + -1] = 0xfa;
              if ((int)uVar17 < 0) {
                bVar2 = (byte)((int)uVar17 >> 0x1f);
                uVar17 = (uint)(byte)-(((byte)uVar17 ^ bVar2) - bVar2);
              }
              auStack_84[iVar19] = (char)uVar17;
              uVar17 = *puVar21;
              if ((int)uVar17 < 0) {
                bVar2 = (byte)((int)uVar17 >> 0x1f);
                uVar17 = (uint)(byte)-(((byte)uVar17 ^ bVar2) - bVar2);
              }
              auStack_84[iVar19 + 1] = (char)uVar17;
              iVar6 = 8;
              *(undefined2 *)(auStack_84 + iVar19 + 2) = 0xf081;
            }
            puVar21 = puVar21 + 3;
            local_6d4 = local_6d4 + 1;
            iVar19 = iVar19 + iVar6;
          } while (local_6d4 < 0xf);
          local_b0[iVar19 + 0x29] = 0xfe;
          local_b0[iVar19 + 0x28] = (cVar3 + '\x02') * '\x02';
          memset(&local_86,0,0x7e);
          puVar21 = (uint *)(iVar15 + 0x4f8);
          _local_88 = 0x100;
          iVar15 = 2;
          local_6d4 = 0xf;
          do {
            uVar17 = puVar21[-1];
            bVar2 = (byte)(*(ushort *)((int)puVar21 + 6) / 10);
            if ((uVar17 == 0) && (*puVar21 == 0)) {
              *(undefined2 *)(local_b0 + iVar15 + 0x29) = 0x81f0;
              local_b0[iVar15 + 0x28] = bVar2 | 1;
              iVar19 = 4;
              auStack_84[iVar15 + -1] = 0xf0;
            }
            else {
              local_b0[iVar15 + 0x29] = 0xf0;
              local_b0[iVar15 + 0x28] = bVar2 | 1;
              if (0x7f < iVar15 + 2U) goto LAB_0041b6e4;
              auStack_84[iVar15 + -2] = 0;
              auStack_84[iVar15 + -1] = 0xfa;
              if ((int)uVar17 < 0) {
                bVar2 = (byte)((int)uVar17 >> 0x1f);
                uVar17 = (uint)(byte)-(((byte)uVar17 ^ bVar2) - bVar2);
              }
              auStack_84[iVar15] = (char)uVar17;
              uVar17 = *puVar21;
              if ((int)uVar17 < 0) {
                bVar2 = (byte)((int)uVar17 >> 0x1f);
                uVar17 = (uint)(byte)-(((byte)uVar17 ^ bVar2) - bVar2);
              }
              auStack_84[iVar15 + 1] = (char)uVar17;
              iVar19 = 8;
              *(undefined2 *)(auStack_84 + iVar15 + 2) = 0xf081;
            }
            puVar21 = puVar21 + 3;
            local_6d4 = local_6d4 + 1;
            iVar15 = iVar15 + iVar19;
          } while (local_6d4 < (int)uVar11);
        }
      }
    }
    local_6e4 = local_6e4 + 1;
    if (0x3f < local_6e4) {
      puVar20 = &local_1d0;
      local_6d4 = 0;
      do {
        memset(&local_d0,0,200);
        cVar14 = (char)local_6d4 + '\x01';
        cVar3 = (((-0x53 - uStack_cc._2_1_) - local_d0._3_1_) - (char)uStack_cc) - uStack_cc._1_1_;
        local_d0._0_2_ = CONCAT11(cVar14,0x12);
        local_d0._0_3_ = CONCAT12(0x40,(undefined2)local_d0);
        uStack_cc = CONCAT13(cVar3 - cVar14,(undefined3)uStack_cc);
        if (*(int *)(param_1 + 0x1af0) != 0) {
          FUN_00414710((byte *)&local_d0);
        }
        (**(code **)(param_1 + 0x788))(&local_d0,8);
        Sleep(10);
        iVar16 = 2;
        do {
          memset(local_b0,0,0xa8);
          local_d0 = *puVar20;
          uStack_cc = puVar20[1];
          uStack_c8 = puVar20[2];
          uStack_c4 = puVar20[3];
          local_c0 = puVar20[4];
          uStack_bc = puVar20[5];
          uStack_b8 = puVar20[6];
          uStack_b4 = puVar20[7];
          (**(code **)(param_1 + 0x798))(&local_d0,0x20);
          Sleep(10);
          puVar20 = puVar20 + 8;
          iVar16 = iVar16 + -1;
        } while (iVar16 != 0);
        local_6d4 = local_6d4 + 1;
      } while (local_6d4 < 4);
      local_6d4 = 0;
      if (0 < local_6e8 + -1) {
        puVar20 = local_6d0;
        do {
          memset(&local_d0,0,200);
          cVar14 = (char)local_6d4 + '\x01';
          cVar3 = ((('l' - uStack_cc._2_1_) - local_d0._3_1_) - (char)uStack_cc) - uStack_cc._1_1_;
          local_d0._0_2_ = CONCAT11(cVar14,0x13);
          local_d0._0_3_ = CONCAT12(0x80,(undefined2)local_d0);
          uStack_cc = CONCAT13(cVar3 - cVar14,(undefined3)uStack_cc);
          if (*(int *)(param_1 + 0x1af0) != 0) {
            FUN_00414710((byte *)&local_d0);
          }
          (**(code **)(param_1 + 0x788))(&local_d0,8);
          Sleep(10);
          iVar16 = 4;
          do {
            memset(local_b0,0,0xa8);
            local_d0 = *puVar20;
            uStack_cc = puVar20[1];
            uStack_c8 = puVar20[2];
            uStack_c4 = puVar20[3];
            local_c0 = puVar20[4];
            uStack_bc = puVar20[5];
            uStack_b8 = puVar20[6];
            uStack_b4 = puVar20[7];
            (**(code **)(param_1 + 0x798))(&local_d0,0x20);
            Sleep(10);
            puVar20 = puVar20 + 8;
            iVar16 = iVar16 + -1;
          } while (iVar16 != 0);
          local_6d4 = local_6d4 + 1;
        } while (local_6d4 < local_6e8 + -1);
      }
      Sleep(10);
      return 1;
    }
  } while( true );
}


