// Program: SM809 mouse Software.exe
// Function: FUN_00420700
// Entry: 00420700
// Body: 00420700 - 004208d0
// Signature: undefined4 FUN_00420700(void)


/* WARNING: Removing unreachable block (ram,0x0042076e) */
/* WARNING: Removing unreachable block (ram,0x00420733) */
/* WARNING: Removing unreachable block (ram,0x004207e5) */

undefined4 FUN_00420700(void)

{
  int *piVar1;
  uint *puVar2;
  int iVar3;
  undefined8 uVar4;
  BOOL BVar5;
  uint uVar6;
  uint uVar7;
  uint uVar8;
  uint in_XCR0;
  
  DAT_00432a60 = 0;
  DAT_0043200c = DAT_0043200c | 1;
  BVar5 = IsProcessorFeaturePresent(10);
  uVar6 = DAT_0043200c;
  if (BVar5 != 0) {
    piVar1 = (int *)cpuid_basic_info(0);
    puVar2 = (uint *)cpuid_Version_info(1);
    uVar7 = puVar2[3];
    if (((piVar1[1] == 0x756e6547 && piVar1[3] == 0x6c65746e) && piVar1[2] == 0x49656e69) &&
       (((((uVar6 = *puVar2 & 0xfff3ff0, uVar6 == 0x106c0 || (uVar6 == 0x20660)) ||
          (uVar6 == 0x20670)) || ((uVar6 == 0x30650 || (uVar6 == 0x30660)))) || (uVar6 == 0x30670)))
       ) {
      DAT_00432a64 = DAT_00432a64 | 1;
    }
    if (*piVar1 < 7) {
      uVar8 = 0;
    }
    else {
      iVar3 = cpuid_Extended_Feature_Enumeration_info(7);
      uVar8 = *(uint *)(iVar3 + 4);
      if ((uVar8 & 0x200) != 0) {
        DAT_00432a64 = DAT_00432a64 | 2;
      }
    }
    DAT_00432a60 = 1;
    uVar6 = DAT_0043200c | 2;
    if ((uVar7 & 0x100000) != 0) {
      uVar6 = DAT_0043200c | 6;
      DAT_00432a60 = 2;
      if (((uVar7 & 0x8000000) != 0) && ((uVar7 & 0x10000000) != 0)) {
        uVar4 = xinuse(0);
        in_XCR0 = in_XCR0 & (uint)uVar4;
        if ((in_XCR0 & 6) == 6) {
          DAT_00432a60 = 3;
          uVar6 = DAT_0043200c | 0xe;
          if ((uVar8 & 0x20) != 0) {
            DAT_00432a60 = 5;
            uVar6 = DAT_0043200c | 0x2e;
            if (((uVar8 & 0xd0030000) == 0xd0030000) && ((in_XCR0 & 0xe0) == 0xe0)) {
              DAT_0043200c = DAT_0043200c | 0x6e;
              DAT_00432a60 = 6;
              uVar6 = DAT_0043200c;
            }
          }
        }
      }
    }
  }
  DAT_0043200c = uVar6;
  return 0;
}


