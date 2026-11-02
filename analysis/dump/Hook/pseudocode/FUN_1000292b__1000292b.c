// Program: Hook.dll
// Function: FUN_1000292b
// Entry: 1000292b
// Body: 1000292b - 1000299f
// Signature: undefined FUN_1000292b(void)


void FUN_1000292b(void)

{
  int iVar1;
  undefined4 *puVar2;
  
  iVar1 = 0;
  if (0 < DAT_10008098) {
    puVar2 = (undefined4 *)((int)DAT_1000809c + 0xc);
    do {
      VirtualFree((LPVOID)*puVar2,0x100000,0x4000);
      VirtualFree((LPVOID)*puVar2,0,0x8000);
      HeapFree(DAT_100092e4,0,(LPVOID)puVar2[1]);
      puVar2 = puVar2 + 5;
      iVar1 = iVar1 + 1;
    } while (iVar1 < DAT_10008098);
  }
  HeapFree(DAT_100092e4,0,DAT_1000809c);
  HeapDestroy(DAT_100092e4);
  return;
}


