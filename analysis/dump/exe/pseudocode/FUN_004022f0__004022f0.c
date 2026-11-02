// Program: SM809 mouse Software.exe
// Function: FUN_004022f0
// Entry: 004022f0
// Body: 004022f0 - 0040236d
// Signature: undefined4 FUN_004022f0(UINT param_1, int * param_2)


undefined4 __fastcall FUN_004022f0(UINT param_1,int *param_2)

{
  UINT UVar1;
  UINT *pUVar2;
  int iVar3;
  
  iVar3 = 0;
  pUVar2 = &DAT_004255e0;
  *param_2 = 0;
  do {
    if (*pUVar2 == param_1) {
      iVar3 = *(int *)(&UNK_004255e4 + iVar3 * 0xc);
      *param_2 = iVar3;
      if (iVar3 - 4U < 0x42) {
        UVar1 = MapVirtualKeyW(param_1,0);
        iVar3 = 0;
        pUVar2 = &DAT_004255e8;
        while (*pUVar2 != UVar1) {
          pUVar2 = pUVar2 + 3;
          iVar3 = iVar3 + 1;
          if (0x425b1b < (int)pUVar2) {
            return 1;
          }
        }
        *param_2 = *(int *)(&UNK_004255e4 + iVar3 * 0xc);
      }
      return 1;
    }
    pUVar2 = pUVar2 + 3;
    iVar3 = iVar3 + 1;
  } while ((int)pUVar2 < 0x425b14);
  return 0;
}


