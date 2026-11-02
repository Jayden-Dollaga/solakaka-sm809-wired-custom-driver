// Program: MSDriver.dll
// Function: FUN_100031cb
// Entry: 100031cb
// Body: 100031cb - 100038eb
// Signature: int FUN_100031cb(int * param_1, byte * param_2, undefined4 * param_3)


int __cdecl FUN_100031cb(int *param_1,byte *param_2,undefined4 *param_3)

{
  WCHAR WVar1;
  byte *pbVar2;
  uint uVar3;
  undefined4 uVar4;
  short *psVar5;
  undefined1 *puVar6;
  WCHAR *pWVar7;
  int *piVar8;
  int iVar9;
  byte bVar10;
  int iVar11;
  ulonglong uVar12;
  undefined8 uVar13;
  longlong lVar14;
  undefined1 local_24c [511];
  undefined1 local_4d;
  undefined4 local_4c;
  undefined4 local_48;
  uint local_44;
  uint local_40;
  CHAR local_3c [4];
  undefined4 local_38;
  int local_34;
  int local_30;
  int local_2c;
  int local_28;
  int local_24;
  int local_20;
  char local_1a;
  char local_19;
  int local_18;
  int local_14;
  undefined1 *local_10;
  WCHAR *local_c;
  uint local_8;
  
  local_34 = 0;
  bVar10 = *param_2;
  local_10 = (undefined1 *)0x0;
  local_18 = 0;
  if (bVar10 != 0) {
    pbVar2 = param_2;
    while (param_2 = pbVar2 + 1, -1 < local_18) {
      if (((char)bVar10 < ' ') || ('x' < (char)bVar10)) {
        uVar3 = 0;
      }
      else {
        uVar3 = *(byte *)((int)&TranslateMessage_exref + (int)(char)bVar10) & 0xf;
      }
      local_34 = (int)(char)(&DAT_10007168)[uVar3 * 8 + local_34] >> 4;
      switch(local_34) {
      case 0:
switchD_10003239_caseD_0:
        local_28 = 0;
        if ((PTR_DAT_10009578[(uint)bVar10 * 2 + 1] & 0x80) != 0) {
          FUN_1000390c((int)(char)bVar10,param_1,&local_18);
          bVar10 = *param_2;
          param_2 = pbVar2 + 2;
        }
        FUN_1000390c((int)(char)bVar10,param_1,&local_18);
        break;
      case 1:
        local_14 = -1;
        local_38 = 0;
        local_2c = 0;
        local_24 = 0;
        local_20 = 0;
        local_8 = 0;
        local_28 = 0;
        break;
      case 2:
        if (bVar10 == 0x20) {
          local_8 = local_8 | 2;
        }
        else if (bVar10 == 0x23) {
          local_8 = local_8 | 0x80;
        }
        else if (bVar10 == 0x2b) {
          local_8 = local_8 | 1;
        }
        else if (bVar10 == 0x2d) {
          local_8 = local_8 | 4;
        }
        else if (bVar10 == 0x30) {
          local_8 = local_8 | 8;
        }
        break;
      case 3:
        if (bVar10 == 0x2a) {
          local_24 = FUN_100039aa((int *)&param_3);
          if (local_24 < 0) {
            local_8 = local_8 | 4;
            local_24 = -local_24;
          }
        }
        else {
          local_24 = (char)bVar10 + -0x30 + local_24 * 10;
        }
        break;
      case 4:
        local_14 = 0;
        break;
      case 5:
        if (bVar10 == 0x2a) {
          local_14 = FUN_100039aa((int *)&param_3);
          if (local_14 < 0) {
            local_14 = -1;
          }
        }
        else {
          local_14 = (char)bVar10 + -0x30 + local_14 * 10;
        }
        break;
      case 6:
        if (bVar10 == 0x49) {
          if ((*param_2 != 0x36) || (pbVar2[2] != 0x34)) {
            local_34 = 0;
            goto switchD_10003239_caseD_0;
          }
          param_2 = pbVar2 + 3;
          local_8 = local_8 | 0x8000;
        }
        else if (bVar10 == 0x68) {
          local_8 = local_8 | 0x20;
        }
        else if (bVar10 == 0x6c) {
          local_8 = local_8 | 0x10;
        }
        else if (bVar10 == 0x77) {
          local_8 = local_8 | 0x800;
        }
        break;
      case 7:
        pWVar7 = local_c;
        if ((char)bVar10 < 'h') {
          if ('d' < (char)bVar10) {
LAB_10003459:
            local_8 = local_8 | 0x40;
            pWVar7 = (WCHAR *)local_24c;
            if (local_14 < 0) {
              local_14 = 6;
            }
            else if ((local_14 == 0) && (bVar10 == 0x67)) {
              local_14 = 1;
            }
            local_4c = *param_3;
            local_48 = param_3[1];
            param_3 = param_3 + 2;
            local_c = pWVar7;
            (*(code *)PTR___fptrap_10009560)
                      (&local_4c,local_24c,(int)(char)bVar10,local_14,local_38);
            uVar3 = local_8 & 0x80;
            if ((uVar3 != 0) && (local_14 == 0)) {
              (*(code *)PTR___fptrap_1000956c)(local_24c);
            }
            if ((bVar10 == 0x67) && (uVar3 == 0)) {
              (*(code *)PTR___fptrap_10009564)(local_24c);
            }
            if (local_24c[0] == '-') {
              local_8 = local_8 | 0x100;
              pWVar7 = (WCHAR *)(local_24c + 1);
              local_c = pWVar7;
            }
LAB_100035cb:
            puVar6 = (undefined1 *)_strlen((char *)pWVar7);
            goto LAB_100037d2;
          }
          if ((char)bVar10 < 'Y') {
            if (bVar10 == 0x58) {
LAB_1000364a:
              local_30 = 7;
LAB_10003651:
              local_10 = (undefined1 *)0x10;
              if ((local_8 & 0x80) != 0) {
                local_1a = '0';
                local_19 = (char)local_30 + 'Q';
                local_20 = 2;
              }
              goto LAB_100036bb;
            }
            if (bVar10 == 0x43) {
              if ((local_8 & 0x830) == 0) {
                local_8 = local_8 | 0x800;
              }
              goto LAB_10003486;
            }
            if ((bVar10 != 0x45) && (bVar10 != 0x47)) {
              if (bVar10 == 0x53) {
                if ((local_8 & 0x830) == 0) {
                  local_8 = local_8 | 0x800;
                }
                goto LAB_100033f8;
              }
              goto LAB_100037d5;
            }
            local_38 = 1;
            bVar10 = bVar10 + 0x20;
            goto LAB_10003459;
          }
          if (bVar10 == 0x5a) {
            psVar5 = (short *)FUN_100039aa((int *)&param_3);
            if ((psVar5 != (short *)0x0) &&
               (local_c = *(WCHAR **)(psVar5 + 2), local_c != (WCHAR *)0x0)) {
              if ((local_8 & 0x800) == 0) {
                local_28 = 0;
                puVar6 = (undefined1 *)(int)*psVar5;
                goto LAB_100037d2;
              }
              local_10 = (undefined1 *)((uint)(int)*psVar5 >> 1);
              local_28 = 1;
              pWVar7 = local_c;
              goto LAB_100037d5;
            }
            local_c = (WCHAR *)PTR_DAT_10009210;
            pWVar7 = (WCHAR *)PTR_DAT_10009210;
            goto LAB_100035cb;
          }
          if (bVar10 == 99) {
LAB_10003486:
            if ((local_8 & 0x810) == 0) {
              uVar4 = FUN_100039aa((int *)&param_3);
              local_24c[0] = (char)uVar4;
              local_10 = (undefined1 *)0x1;
            }
            else {
              uVar4 = FUN_100039c7((int *)&param_3);
              local_10 = (undefined1 *)FUN_10004cab(local_24c,(WCHAR)uVar4);
              if ((int)local_10 < 0) {
                local_2c = 1;
              }
            }
            pWVar7 = (WCHAR *)local_24c;
          }
          else if (bVar10 == 100) goto LAB_100036b0;
        }
        else {
          if (bVar10 == 0x69) {
LAB_100036b0:
            local_8 = local_8 | 0x40;
LAB_100036b4:
            local_10 = (undefined1 *)0xa;
LAB_100036bb:
            if ((local_8 & 0x8000) == 0) {
              if ((local_8 & 0x20) == 0) {
                if ((local_8 & 0x40) == 0) {
                  uVar3 = FUN_100039aa((int *)&param_3);
                  uVar12 = (ulonglong)uVar3;
                  goto LAB_1000370e;
                }
                uVar3 = FUN_100039aa((int *)&param_3);
              }
              else if ((local_8 & 0x40) == 0) {
                uVar3 = FUN_100039aa((int *)&param_3);
                uVar3 = uVar3 & 0xffff;
              }
              else {
                uVar4 = FUN_100039aa((int *)&param_3);
                uVar3 = (uint)(short)uVar4;
              }
              uVar12 = (ulonglong)(int)uVar3;
            }
            else {
              uVar12 = FUN_100039b7((int *)&param_3);
            }
LAB_1000370e:
            iVar11 = (int)(uVar12 >> 0x20);
            if ((((local_8 & 0x40) != 0) && (iVar11 == 0 || (longlong)uVar12 < 0)) &&
               ((longlong)uVar12 < 0)) {
              local_8 = local_8 | 0x100;
              uVar12 = CONCAT44(-(iVar11 + (uint)((int)uVar12 != 0)),-(int)uVar12);
            }
            iVar11 = (int)(uVar12 >> 0x20);
            if ((local_8 & 0x8000) == 0) {
              iVar11 = 0;
            }
            lVar14 = CONCAT44(iVar11,(int)uVar12);
            if (local_14 < 0) {
              local_14 = 1;
            }
            else {
              local_8 = local_8 & 0xfffffff7;
            }
            if ((int)uVar12 == 0 && iVar11 == 0) {
              local_20 = 0;
            }
            local_c = (WCHAR *)&local_4d;
            while ((iVar11 = local_14 + -1, 0 < local_14 || (lVar14 != 0))) {
              local_40 = (int)local_10 >> 0x1f;
              local_44 = (uint)local_10;
              uVar3 = (uint)((ulonglong)lVar14 >> 0x20);
              local_14 = iVar11;
              uVar13 = __aullrem((uint)lVar14,uVar3,(uint)local_10,local_40);
              iVar11 = (int)uVar13 + 0x30;
              lVar14 = __aulldiv((uint)lVar14,uVar3,local_44,local_40);
              if (0x39 < iVar11) {
                iVar11 = iVar11 + local_30;
              }
              pWVar7 = (WCHAR *)((int)local_c + -1);
              *(char *)local_c = (char)iVar11;
              local_c = pWVar7;
            }
            local_10 = local_24c + -(int)local_c + 0x1ff;
            pWVar7 = (WCHAR *)((int)local_c + 1);
            local_14 = iVar11;
            if ((local_8 & 0x200) == 0) goto LAB_100037d5;
            if (*(char *)pWVar7 == '0') {
              if (local_10 != (undefined1 *)0x0) goto LAB_100037d5;
            }
            puVar6 = local_24c + -(int)local_c + 0x200;
            *(char *)local_c = '0';
          }
          else {
            if (bVar10 == 0x6e) {
              piVar8 = (int *)FUN_100039aa((int *)&param_3);
              if ((local_8 & 0x20) == 0) {
                *piVar8 = local_18;
              }
              else {
                *(undefined2 *)piVar8 = (undefined2)local_18;
              }
              local_2c = 1;
              break;
            }
            if (bVar10 == 0x6f) {
              local_10 = (undefined1 *)0x8;
              if ((local_8 & 0x80) != 0) {
                local_8 = local_8 | 0x200;
              }
              goto LAB_100036bb;
            }
            if (bVar10 == 0x70) {
              local_14 = 8;
              goto LAB_1000364a;
            }
            if (bVar10 != 0x73) {
              if (bVar10 != 0x75) {
                if (bVar10 != 0x78) goto LAB_100037d5;
                local_30 = 0x27;
                goto LAB_10003651;
              }
              goto LAB_100036b4;
            }
LAB_100033f8:
            iVar11 = local_14;
            if (local_14 == -1) {
              iVar11 = 0x7fffffff;
            }
            local_c = (WCHAR *)FUN_100039aa((int *)&param_3);
            if ((local_8 & 0x810) == 0) {
              if (local_c == (WCHAR *)0x0) {
                local_c = (WCHAR *)PTR_DAT_10009210;
              }
              for (pWVar7 = local_c; (iVar11 != 0 && ((char)*pWVar7 != '\0'));
                  pWVar7 = (WCHAR *)((int)pWVar7 + 1)) {
                iVar11 = iVar11 + -1;
              }
              puVar6 = (undefined1 *)((int)pWVar7 - (int)local_c);
            }
            else {
              if (local_c == (WCHAR *)0x0) {
                local_c = (WCHAR *)PTR_DAT_10009214;
              }
              local_28 = 1;
              for (pWVar7 = local_c; (iVar11 != 0 && (*pWVar7 != L'\0')); pWVar7 = pWVar7 + 1) {
                iVar11 = iVar11 + -1;
              }
              puVar6 = (undefined1 *)((int)pWVar7 - (int)local_c >> 1);
            }
          }
LAB_100037d2:
          local_10 = puVar6;
          pWVar7 = local_c;
        }
LAB_100037d5:
        local_c = pWVar7;
        uVar3 = local_8;
        if (local_2c == 0) {
          if ((local_8 & 0x40) != 0) {
            if ((local_8 & 0x100) == 0) {
              if ((local_8 & 1) == 0) {
                if ((local_8 & 2) == 0) goto LAB_1000380d;
                local_1a = ' ';
              }
              else {
                local_1a = '+';
              }
            }
            else {
              local_1a = '-';
            }
            local_20 = 1;
          }
LAB_1000380d:
          iVar11 = (local_24 - local_20) - (int)local_10;
          if ((local_8 & 0xc) == 0) {
            FUN_10003941(0x20,iVar11,param_1,&local_18);
          }
          FUN_10003972(&local_1a,local_20,param_1,&local_18);
          if (((uVar3 & 8) != 0) && ((uVar3 & 4) == 0)) {
            FUN_10003941(0x30,iVar11,param_1,&local_18);
          }
          if ((local_28 == 0) || ((int)local_10 < 1)) {
            FUN_10003972((char *)local_c,(int)local_10,param_1,&local_18);
          }
          else {
            puVar6 = local_10;
            pWVar7 = local_c;
            do {
              puVar6 = puVar6 + -1;
              WVar1 = *pWVar7;
              pWVar7 = pWVar7 + 1;
              iVar9 = FUN_10004cab(local_3c,WVar1);
              if (iVar9 < 1) break;
              FUN_10003972(local_3c,iVar9,param_1,&local_18);
            } while (puVar6 != (undefined1 *)0x0);
          }
          if ((local_8 & 4) != 0) {
            FUN_10003941(0x20,iVar11,param_1,&local_18);
          }
        }
      }
      bVar10 = *param_2;
      if (bVar10 == 0) {
        return local_18;
      }
      pbVar2 = param_2;
    }
  }
  return local_18;
}


