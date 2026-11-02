// Program: MSDriver.dll
// Function: FUN_10004f50
// Entry: 10004f50
// Body: 10004f50 - 100050fc
// Signature: undefined4 FUN_10004f50(int param_1)


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 __cdecl FUN_10004f50(int param_1)

{
  BYTE *pBVar1;
  byte *pbVar2;
  byte bVar3;
  byte bVar4;
  UINT CodePage;
  UINT *pUVar5;
  BOOL BVar6;
  uint uVar7;
  uint uVar8;
  BYTE *pBVar9;
  int iVar10;
  byte *pbVar11;
  int iVar12;
  byte *pbVar13;
  undefined4 uVar14;
  undefined4 *puVar15;
  _cpinfo local_1c;
  uint local_8;
  
  FUN_1000277c(0x19);
  CodePage = FUN_100050fd(param_1);
  if (CodePage != DAT_1000a258) {
    if (CodePage != 0) {
      iVar12 = 0;
      pUVar5 = &DAT_10009828;
LAB_10004f8d:
      if (*pUVar5 != CodePage) goto code_r0x10004f91;
      local_8 = 0;
      puVar15 = &DAT_1000a380;
      for (iVar10 = 0x40; iVar10 != 0; iVar10 = iVar10 + -1) {
        *puVar15 = 0;
        puVar15 = puVar15 + 1;
      }
      iVar12 = iVar12 * 0x30;
      *(undefined1 *)puVar15 = 0;
      pbVar13 = (byte *)(iVar12 + 0x10009838);
      do {
        bVar3 = *pbVar13;
        pbVar11 = pbVar13;
        while ((bVar3 != 0 && (bVar3 = pbVar11[1], bVar3 != 0))) {
          uVar8 = (uint)*pbVar11;
          if (uVar8 <= bVar3) {
            bVar4 = (&DAT_10009820)[local_8];
            do {
              pbVar2 = (byte *)((int)&DAT_1000a380 + uVar8 + 1);
              *pbVar2 = *pbVar2 | bVar4;
              uVar8 = uVar8 + 1;
            } while (uVar8 <= bVar3);
          }
          pbVar11 = pbVar11 + 2;
          bVar3 = *pbVar11;
        }
        local_8 = local_8 + 1;
        pbVar13 = pbVar13 + 8;
      } while (local_8 < 4);
      _DAT_1000a26c = 1;
      DAT_1000a258 = CodePage;
      DAT_1000a484 = FUN_10005147(CodePage);
      DAT_1000a260 = *(undefined4 *)(iVar12 + 0x1000982c);
      DAT_1000a264 = *(undefined4 *)(iVar12 + 0x10009830);
      DAT_1000a268 = *(undefined4 *)(iVar12 + 0x10009834);
      goto LAB_100050e1;
    }
    goto LAB_100050dc;
  }
  goto LAB_10004f77;
code_r0x10004f91:
  pUVar5 = pUVar5 + 0xc;
  iVar12 = iVar12 + 1;
  if (0x10009917 < (int)pUVar5) goto code_r0x10004f9c;
  goto LAB_10004f8d;
code_r0x10004f9c:
  BVar6 = GetCPInfo(CodePage,&local_1c);
  uVar8 = 1;
  if (BVar6 == 1) {
    DAT_1000a484 = 0;
    puVar15 = &DAT_1000a380;
    for (iVar12 = 0x40; iVar12 != 0; iVar12 = iVar12 + -1) {
      *puVar15 = 0;
      puVar15 = puVar15 + 1;
    }
    *(undefined1 *)puVar15 = 0;
    if (local_1c.MaxCharSize < 2) {
      _DAT_1000a26c = 0;
      DAT_1000a258 = CodePage;
    }
    else {
      DAT_1000a258 = CodePage;
      if (local_1c.LeadByte[0] != '\0') {
        pBVar9 = local_1c.LeadByte + 1;
        do {
          bVar3 = *pBVar9;
          if (bVar3 == 0) break;
          for (uVar7 = (uint)pBVar9[-1]; uVar7 <= bVar3; uVar7 = uVar7 + 1) {
            pbVar13 = (byte *)((int)&DAT_1000a380 + uVar7 + 1);
            *pbVar13 = *pbVar13 | 4;
          }
          pBVar1 = pBVar9 + 1;
          pBVar9 = pBVar9 + 2;
        } while (*pBVar1 != 0);
      }
      do {
        pbVar13 = (byte *)((int)&DAT_1000a380 + uVar8 + 1);
        *pbVar13 = *pbVar13 | 8;
        uVar8 = uVar8 + 1;
      } while (uVar8 < 0xff);
      DAT_1000a484 = FUN_10005147(CodePage);
      _DAT_1000a26c = 1;
    }
    DAT_1000a260 = 0;
    DAT_1000a264 = 0;
    DAT_1000a268 = 0;
  }
  else {
    if (DAT_1000a0cc == 0) {
      uVar14 = 0xffffffff;
      goto LAB_100050ee;
    }
LAB_100050dc:
    FUN_1000517a();
  }
LAB_100050e1:
  FUN_100051a3();
LAB_10004f77:
  uVar14 = 0;
LAB_100050ee:
  FUN_100027dd(0x19);
  return uVar14;
}


