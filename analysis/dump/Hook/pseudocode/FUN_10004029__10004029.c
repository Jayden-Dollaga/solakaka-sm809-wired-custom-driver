// Program: Hook.dll
// Function: FUN_10004029
// Entry: 10004029
// Body: 10004029 - 10004331
// Signature: int * FUN_10004029(uint * param_1)


int * __cdecl FUN_10004029(uint *param_1)

{
  uint *puVar1;
  char *pcVar2;
  int *piVar3;
  char cVar4;
  int *piVar5;
  byte bVar6;
  uint uVar7;
  int iVar8;
  int iVar9;
  uint *puVar10;
  int iVar11;
  int *piVar12;
  uint uVar13;
  uint local_10;
  uint local_c;
  int local_8;
  
  puVar10 = DAT_1000809c + DAT_10008098 * 5;
  uVar7 = (int)param_1 + 0x17U & 0xfffffff0;
  iVar8 = (int)((int)param_1 + 0x17U) >> 4;
  iVar9 = iVar8 + -1;
  if (iVar9 < 0x20) {
    local_10 = 0xffffffff >> ((byte)iVar9 & 0x1f);
    local_c = 0xffffffff;
  }
  else {
    local_c = 0xffffffff >> ((char)iVar8 - 0x21U & 0x1f);
    local_10 = 0;
  }
  for (param_1 = DAT_10008090;
      (param_1 < puVar10 && ((param_1[1] & local_c) == 0 && (*param_1 & local_10) == 0));
      param_1 = param_1 + 5) {
  }
  if (param_1 == puVar10) {
    for (param_1 = DAT_1000809c;
        (param_1 < DAT_10008090 && ((param_1[1] & local_c) == 0 && (*param_1 & local_10) == 0));
        param_1 = param_1 + 5) {
    }
    if (param_1 == DAT_10008090) {
      for (; (param_1 < puVar10 && (param_1[2] == 0)); param_1 = param_1 + 5) {
      }
      if (param_1 == puVar10) {
        for (param_1 = DAT_1000809c; (param_1 < DAT_10008090 && (param_1[2] == 0));
            param_1 = param_1 + 5) {
        }
        if ((param_1 == DAT_10008090) && (param_1 = FUN_10004332(), param_1 == (uint *)0x0)) {
          return (int *)0x0;
        }
      }
      iVar8 = FUN_100043e3((int)param_1);
      *(int *)param_1[4] = iVar8;
      if (*(int *)param_1[4] == -1) {
        return (int *)0x0;
      }
    }
  }
  piVar5 = (int *)param_1[4];
  local_8 = *piVar5;
  if ((local_8 == -1) ||
     ((piVar5[local_8 + 0x31] & local_c) == 0 && (piVar5[local_8 + 0x11] & local_10) == 0)) {
    local_8 = 0;
    puVar10 = (uint *)(piVar5 + 0x11);
    if ((piVar5[0x31] & local_c) == 0 && (piVar5[0x11] & local_10) == 0) {
      do {
        puVar1 = puVar10 + 0x21;
        local_8 = local_8 + 1;
        puVar10 = puVar10 + 1;
      } while ((*puVar1 & local_c) == 0 && (local_10 & *puVar10) == 0);
    }
  }
  iVar8 = 0;
  piVar3 = piVar5 + local_8 * 0x81 + 0x51;
  local_10 = piVar5[local_8 + 0x11] & local_10;
  if (local_10 == 0) {
    local_10 = piVar5[local_8 + 0x31] & local_c;
    iVar8 = 0x20;
  }
  for (; -1 < (int)local_10; local_10 = local_10 << 1) {
    iVar8 = iVar8 + 1;
  }
  piVar12 = (int *)piVar3[iVar8 * 2 + 1];
  iVar11 = *piVar12 - uVar7;
  iVar9 = (iVar11 >> 4) + -1;
  if (0x3f < iVar9) {
    iVar9 = 0x3f;
  }
  DAT_10008090 = param_1;
  if (iVar9 != iVar8) {
    if (piVar12[1] == piVar12[2]) {
      if (iVar8 < 0x20) {
        pcVar2 = (char *)((int)piVar5 + iVar8 + 4);
        uVar13 = ~(0x80000000U >> ((byte)iVar8 & 0x1f));
        piVar5[local_8 + 0x11] = uVar13 & piVar5[local_8 + 0x11];
        *pcVar2 = *pcVar2 + -1;
        if (*pcVar2 == '\0') {
          *param_1 = *param_1 & uVar13;
        }
      }
      else {
        pcVar2 = (char *)((int)piVar5 + iVar8 + 4);
        uVar13 = ~(0x80000000U >> ((byte)iVar8 - 0x20 & 0x1f));
        piVar5[local_8 + 0x31] = piVar5[local_8 + 0x31] & uVar13;
        *pcVar2 = *pcVar2 + -1;
        if (*pcVar2 == '\0') {
          param_1[1] = param_1[1] & uVar13;
        }
      }
    }
    *(int *)(piVar12[2] + 4) = piVar12[1];
    *(int *)(piVar12[1] + 8) = piVar12[2];
    if (iVar11 == 0) goto LAB_100042ef;
    piVar12[1] = piVar3[iVar9 * 2 + 1];
    piVar12[2] = (int)(piVar3 + iVar9 * 2);
    (piVar3 + iVar9 * 2)[1] = (int)piVar12;
    *(int **)(piVar12[1] + 8) = piVar12;
    if (piVar12[1] == piVar12[2]) {
      cVar4 = *(char *)(iVar9 + 4 + (int)piVar5);
      bVar6 = (byte)iVar9;
      if (iVar9 < 0x20) {
        *(char *)(iVar9 + 4 + (int)piVar5) = cVar4 + '\x01';
        if (cVar4 == '\0') {
          *param_1 = *param_1 | 0x80000000U >> (bVar6 & 0x1f);
        }
        piVar5[local_8 + 0x11] = piVar5[local_8 + 0x11] | 0x80000000U >> (bVar6 & 0x1f);
      }
      else {
        *(char *)(iVar9 + 4 + (int)piVar5) = cVar4 + '\x01';
        if (cVar4 == '\0') {
          param_1[1] = param_1[1] | 0x80000000U >> (bVar6 - 0x20 & 0x1f);
        }
        piVar5[local_8 + 0x31] = piVar5[local_8 + 0x31] | 0x80000000U >> (bVar6 - 0x20 & 0x1f);
      }
    }
  }
  if (iVar11 != 0) {
    *piVar12 = iVar11;
    *(int *)(iVar11 + -4 + (int)piVar12) = iVar11;
  }
LAB_100042ef:
  piVar12 = (int *)((int)piVar12 + iVar11);
  *piVar12 = uVar7 + 1;
  *(uint *)((int)piVar12 + (uVar7 - 4)) = uVar7 + 1;
  iVar8 = *piVar3;
  *piVar3 = iVar8 + 1;
  if (((iVar8 == 0) && (param_1 == DAT_10008094)) && (local_8 == DAT_1000808c)) {
    DAT_10008094 = (uint *)0x0;
  }
  *piVar5 = local_8;
  return piVar12 + 1;
}


