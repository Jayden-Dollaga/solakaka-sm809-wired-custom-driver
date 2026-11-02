// Program: SM809 mouse Software.exe
// Function: FUN_004040e0
// Entry: 004040e0
// Body: 004040e0 - 004041f4
// Signature: undefined4 FUN_004040e0(uint param_1, int param_2, undefined4 param_3, undefined4 param_4, int param_5)


undefined4 __fastcall
FUN_004040e0(uint param_1,int param_2,undefined4 param_3,undefined4 param_4,int param_5)

{
  int iVar1;
  int *piVar2;
  int iVar3;
  undefined2 *puVar4;
  undefined4 *puVar5;
  undefined4 uVar6;
  undefined4 *puVar7;
  undefined1 *local_10;
  undefined4 local_c;
  int local_8;
  
  uVar6 = 0;
  local_c = 0;
  local_8 = 0;
  piVar2 = DAT_0046c38c;
  if (DAT_0046c38c != DAT_0046c390) {
    do {
      local_10 = &DAT_00425c18;
      puVar4 = (undefined2 *)(*piVar2 + 0x232);
      do {
        if (param_1 == *(uint *)(puVar4 + -9)) {
          if (((param_5 == 0) && (DAT_0046c380 != DAT_0046c384)) && (-1 < (int)param_1)) {
            if ((uint)(DAT_0046c384 - DAT_0046c380 >> 2) <= param_1) {
                    /* WARNING: Subroutine does not return */
              FUN_004050f0();
            }
            iVar1 = *(int *)(DAT_0046c380 + param_1 * 4);
            if (iVar1 == 0) goto LAB_0040419b;
            *puVar4 = *(undefined2 *)(iVar1 + 0xcc);
            puVar5 = (undefined4 *)(iVar1 + 0xd8);
            puVar7 = (undefined4 *)(puVar4 + 0x1bd);
            for (iVar3 = 0xa0; iVar3 != 0; iVar3 = iVar3 + -1) {
              *puVar7 = *puVar5;
              puVar5 = puVar5 + 1;
              puVar7 = puVar7 + 1;
            }
            *(uint *)(puVar4 + 1) = (uint)*(ushort *)(iVar1 + 200);
            wcscpy_s(puVar4 + -0x3f,0x32,(wchar_t *)(iVar1 + 100));
            uVar6 = local_c;
          }
          else {
LAB_0040419b:
            *(undefined1 *)((int)puVar4 + -0x19) = *local_10;
          }
          if (param_2 == local_8) {
            uVar6 = 1;
          }
          local_c = uVar6;
        }
        local_10 = local_10 + 4;
        puVar4 = puVar4 + 0x396;
      } while ((int)local_10 < 0x425c98);
      local_8 = local_8 + 1;
      piVar2 = piVar2 + 1;
    } while (piVar2 != DAT_0046c390);
  }
  return uVar6;
}


