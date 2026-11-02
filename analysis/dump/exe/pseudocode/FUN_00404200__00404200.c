// Program: SM809 mouse Software.exe
// Function: FUN_00404200
// Entry: 00404200
// Body: 00404200 - 0040430f
// Signature: undefined4 FUN_00404200(uint param_1, int param_2, undefined4 param_3, undefined4 param_4, int param_5)


undefined4 __fastcall
FUN_00404200(uint param_1,int param_2,undefined4 param_3,undefined4 param_4,int param_5)

{
  int iVar1;
  int *piVar2;
  int iVar3;
  undefined1 *puVar4;
  undefined4 uVar5;
  undefined4 *puVar6;
  undefined4 *puVar7;
  int local_14;
  undefined4 local_10;
  undefined1 *local_8;
  
  uVar5 = 0;
  local_10 = 0;
  local_14 = 0;
  piVar2 = DAT_0046c38c;
  if (DAT_0046c38c != DAT_0046c390) {
    do {
      local_8 = &DAT_00425c18;
      puVar4 = (undefined1 *)(*piVar2 + 0x219);
      do {
        if (param_1 == *(uint *)(puVar4 + 3)) {
          if (param_5 == 0) {
            if ((DAT_0046c398 != DAT_0046c39c) && (-1 < (int)param_1)) {
              if ((uint)(DAT_0046c39c - DAT_0046c398 >> 2) <= param_1) {
                    /* WARNING: Subroutine does not return */
                FUN_004050f0();
              }
              iVar1 = *(int *)(DAT_0046c398 + param_1 * 4);
              if (iVar1 != 0) {
                *(ushort *)(puVar4 + 0x19) = (ushort)*(byte *)(iVar1 + 200);
                *(uint *)(puVar4 + 0x1b) = (uint)*(byte *)(iVar1 + 0xca);
                puVar6 = (undefined4 *)(iVar1 + 0xd8);
                puVar7 = (undefined4 *)(puVar4 + 0x227);
                for (iVar3 = 0x5a; iVar3 != 0; iVar3 = iVar3 + -1) {
                  *puVar7 = *puVar6;
                  puVar6 = puVar6 + 1;
                  puVar7 = puVar7 + 1;
                }
                wcscpy_s((wchar_t *)(puVar4 + -0x65),0x32,(wchar_t *)(iVar1 + 100));
                uVar5 = local_10;
              }
            }
          }
          else {
            *puVar4 = *local_8;
          }
          if (param_2 == local_14) {
            uVar5 = 1;
          }
          local_10 = uVar5;
        }
        local_8 = local_8 + 4;
        puVar4 = puVar4 + 0x72c;
      } while ((int)local_8 < 0x425c98);
      local_14 = local_14 + 1;
      piVar2 = piVar2 + 1;
    } while (piVar2 != DAT_0046c390);
  }
  return uVar5;
}


