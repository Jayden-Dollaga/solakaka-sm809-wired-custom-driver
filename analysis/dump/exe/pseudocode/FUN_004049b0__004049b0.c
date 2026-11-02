// Program: SM809 mouse Software.exe
// Function: FUN_004049b0
// Entry: 004049b0
// Body: 004049b0 - 00404bfa
// Signature: uint FUN_004049b0(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */
/* WARNING: Type propagation algorithm not settling */

uint __fastcall FUN_004049b0(int param_1)

{
  byte *pbVar1;
  int iVar2;
  char cVar3;
  uint uVar4;
  int iVar5;
  char *******pppppppcVar6;
  char *pcVar7;
  uint local_44;
  byte *local_3c;
  char *local_38;
  undefined4 local_34;
  char *******local_30 [4];
  uint local_20;
  uint local_1c;
  byte local_15;
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  char ******local_8;
  
  local_8 = (char ******)0xffffffff;
  puStack_c = &LAB_0042148d;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_30 + 0xb);
  uVar4 = **(uint **)(param_1 + 0x1c);
  if (uVar4 != 0) {
    iVar5 = **(int **)(param_1 + 0x2c);
    if (uVar4 < iVar5 + uVar4) {
      **(int **)(param_1 + 0x2c) = iVar5 + -1;
      pbVar1 = (byte *)**(int **)(param_1 + 0x1c);
      **(int **)(param_1 + 0x1c) = (int)(pbVar1 + 1);
      return (uint)*pbVar1;
    }
  }
  if (*(int *)(param_1 + 0x4c) != 0) {
    ExceptionList = &local_10;
    if (**(int **)(param_1 + 0xc) == param_1 + 0x3c) {
      iVar5 = *(int *)(param_1 + 0x54);
      iVar2 = *(int *)(param_1 + 0x50);
      **(int **)(param_1 + 0xc) = iVar2;
      **(int **)(param_1 + 0x1c) = iVar2;
      **(int **)(param_1 + 0x2c) = iVar5 - iVar2;
    }
    if (*(int *)(param_1 + 0x38) != 0) {
      local_20 = 0;
      local_1c = 0xf;
      local_30[0] = (char *******)0x0;
      local_8 = (char ******)0x0;
      iVar5 = fgetc(*(FILE **)(param_1 + 0x4c));
      do {
        uVar4 = local_20;
        if (iVar5 == -1) {
LAB_00404ba4:
          uVar4 = 0xffffffff;
LAB_00404ba7:
          if (0xf < local_1c) {
            pppppppcVar6 = local_30[0];
            if ((0xfff < local_1c + 1) &&
               (pppppppcVar6 = (char *******)local_30[0][-1],
               (char *)0x1f < (char *)((int)local_30[0] + (-4 - (int)pppppppcVar6)))) {
                    /* WARNING: Subroutine does not return */
              _invalid_parameter_noinfo_noreturn();
            }
            FUN_0041feb7(pppppppcVar6);
          }
          ExceptionList = local_10;
          return uVar4;
        }
        cVar3 = (char)iVar5;
        local_34 = CONCAT31(local_34._1_3_,cVar3);
        if (local_20 < local_1c) {
          pppppppcVar6 = (char *******)local_30;
          if (0xf < local_1c) {
            pppppppcVar6 = local_30[0];
          }
          pcVar7 = (char *)((int)pppppppcVar6 + local_20);
          local_20 = local_20 + 1;
          *pcVar7 = cVar3;
          *(char *)((int)pppppppcVar6 + uVar4 + 1) = '\0';
        }
        else {
          local_44 = local_44 & 0xffffff00;
          FUN_00405a30(local_30,local_20,local_44,cVar3);
        }
        pppppppcVar6 = (char *******)local_30;
        if (0xf < local_1c) {
          pppppppcVar6 = local_30[0];
        }
        iVar5 = std::codecvt<char,char,_Mbstatet>::in
                          (*(codecvt<char,char,_Mbstatet> **)(param_1 + 0x38),
                           (_Mbstatet *)(param_1 + 0x40),(char *)pppppppcVar6,
                           (char *)((int)pppppppcVar6 + local_20),&local_38,(char *)&local_15,
                           (char *)&local_14,(char **)&local_3c);
        if ((iVar5 != 0) && (iVar5 != 1)) {
          if (iVar5 == 3) {
            pppppppcVar6 = (char *******)local_30;
            if (0xf < local_1c) {
              pppppppcVar6 = local_30[0];
            }
            uVar4 = (uint)*(char *)pppppppcVar6;
            goto LAB_00404ba7;
          }
          goto LAB_00404ba4;
        }
        if (local_3c != &local_15) {
          pppppppcVar6 = (char *******)local_30;
          if (0xf < local_1c) {
            pppppppcVar6 = local_30[0];
          }
          for (pcVar7 = (char *)((int)pppppppcVar6 + (local_20 - (int)local_38)); 0 < (int)pcVar7;
              pcVar7 = pcVar7 + -1) {
            ungetc((int)(pcVar7 + -1)[(int)local_38],*(FILE **)(param_1 + 0x4c));
          }
          uVar4 = (uint)local_15;
          goto LAB_00404ba7;
        }
        pppppppcVar6 = (char *******)local_30;
        if (0xf < local_1c) {
          pppppppcVar6 = local_30[0];
        }
        uVar4 = (int)local_38 - (int)pppppppcVar6;
        if (local_20 < (uint)((int)local_38 - (int)pppppppcVar6)) {
          uVar4 = local_20;
        }
        pppppppcVar6 = (char *******)local_30;
        if (0xf < local_1c) {
          pppppppcVar6 = local_30[0];
        }
        local_20 = local_20 - uVar4;
        memmove(pppppppcVar6,(char *)((int)pppppppcVar6 + uVar4),local_20 + 1);
        iVar5 = fgetc(*(FILE **)(param_1 + 0x4c));
      } while( true );
    }
    uVar4 = fgetc(*(FILE **)(param_1 + 0x4c));
    if (uVar4 != 0xffffffff) {
      ExceptionList = local_10;
      return uVar4 & 0xff;
    }
  }
  ExceptionList = local_10;
  return 0xffffffff;
}


