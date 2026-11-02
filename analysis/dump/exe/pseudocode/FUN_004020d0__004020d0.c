// Program: SM809 mouse Software.exe
// Function: FUN_004020d0
// Entry: 004020d0
// Body: 004020d0 - 004022e6
// Signature: undefined FUN_004020d0(int param_1, int param_2)


void __fastcall FUN_004020d0(int param_1,int param_2)

{
  undefined1 *puVar1;
  undefined4 uVar2;
  undefined4 *puVar3;
  undefined1 *puVar4;
  int iVar5;
  int local_8;
  
  local_8 = 8;
  iVar5 = 0;
  *(undefined4 *)(param_1 + 100) = 6;
  puVar4 = (undefined1 *)(param_1 + 0x108);
  *(undefined4 *)(param_1 + 0x68) = 3;
  puVar3 = (undefined4 *)(param_1 + 0xa8);
  *(undefined4 *)(param_1 + 0x6c) = 5;
  *(undefined4 *)(param_1 + 0x70) = 0;
  *(undefined4 *)(param_1 + 0x74) = 0;
  *(undefined4 *)(param_1 + 0x78) = 10;
  *(undefined4 *)(param_1 + 0x7c) = 10;
  *(undefined4 *)(param_1 + 0x80) = 2;
  *(undefined4 *)(param_1 + 0x84) = 0;
  do {
    if ((((param_2 == 0xcfd) || (param_2 == 0xcff)) || (param_2 == 0xd07)) ||
       ((param_2 == 0xd05 || (param_2 == 0xcef)))) {
LAB_004021a6:
      uVar2 = *(undefined4 *)(&UNK_00425dc8 + iVar5 * 4);
LAB_004021ad:
      puVar3[-8] = uVar2;
      *puVar3 = uVar2;
    }
    else {
      if (param_2 == 0xc8c) {
        uVar2 = (&DAT_00425da8)[iVar5];
        goto LAB_004021ad;
      }
      if (param_2 == 0xc20) {
        uVar2 = *(undefined4 *)(&UNK_00425d88 + iVar5 * 4);
        goto LAB_004021ad;
      }
      if (param_2 == 0xbea) {
        uVar2 = *(undefined4 *)(&UNK_00425d68 + iVar5 * 4);
        goto LAB_004021ad;
      }
      if ((param_2 != 0x13ba) && ((param_2 == 0x1900 || (param_2 == 0xd02)))) goto LAB_004021a6;
    }
    puVar4[-0x40] = (&DAT_00425d60)[iVar5];
    puVar3[10] = (&DAT_00425d40)[iVar5];
    puVar3[0x1a] = (&DAT_00425d20)[iVar5];
    puVar3 = puVar3 + 1;
    puVar1 = &DAT_00425d18 + iVar5;
    iVar5 = iVar5 + 1;
    *puVar4 = *puVar1;
    puVar4 = puVar4 + 1;
    local_8 = local_8 + -1;
    if (local_8 == 0) {
      *(undefined4 *)(param_1 + 0xf0) = 4;
      *(undefined4 *)(param_1 + 0xfc) = 1;
      *(undefined4 *)(param_1 + 0x104) = 0xff;
      *(undefined4 *)(param_1 + 0xf4) = 0xff;
      *(undefined4 *)(param_1 + 0xf8) = 3;
      *(undefined4 *)(param_1 + 0x100) = 2;
      *(undefined4 *)(param_1 + 0x130) = 0x10;
      *(undefined4 *)(param_1 + 0x14c) = 0;
      *(undefined4 *)(param_1 + 0x138) = 0;
      *(undefined4 *)(param_1 + 0x13c) = 0;
      *(undefined4 *)(param_1 + 0x140) = 0;
      *(undefined4 *)(param_1 + 0x144) = 0;
      *(undefined4 *)(param_1 + 0x148) = 0;
      *(undefined2 *)(param_1 + 0x138) = 0x804;
      memset((void *)(param_1 + 0x150),0,0x1cb00);
      iVar5 = 0;
      puVar4 = (undefined1 *)(param_1 + 0x219);
      do {
        *puVar4 = (&DAT_00425c18)[iVar5 * 4];
        puVar4[1] = (&DAT_00425b18)[iVar5 * 4];
        puVar4[-1] = (char)iVar5;
        wcscpy_s((wchar_t *)(puVar4 + -0x65),0x32,L"");
        iVar5 = iVar5 + 1;
        *(undefined4 *)(puVar4 + 0x38f) = 0xff;
        *(undefined4 *)(puVar4 + 7) = 0xffffffff;
        *(undefined4 *)(puVar4 + 3) = 0xffffffff;
        *(undefined4 *)(puVar4 + 0x613) = 0;
        *(undefined4 *)(puVar4 + 0x617) = 2;
        puVar4 = puVar4 + 0x72c;
      } while (iVar5 < 0x40);
      return;
    }
  } while( true );
}


