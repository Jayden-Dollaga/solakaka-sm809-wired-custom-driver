// Program: MSDriver.dll
// Function: FUN_10002672
// Entry: 10002672
// Body: 10002672 - 100026e6
// Signature: undefined FUN_10002672(void)


void FUN_10002672(void)

{
  int iVar1;
  undefined4 *puVar2;
  
  iVar1 = 0;
  if (0 < DAT_1000b5e8) {
    puVar2 = (undefined4 *)((int)DAT_1000b5ec + 0xc);
    do {
      VirtualFree((LPVOID)*puVar2,0x100000,0x4000);
      VirtualFree((LPVOID)*puVar2,0,0x8000);
      HeapFree(DAT_1000b5f0,0,(LPVOID)puVar2[1]);
      puVar2 = puVar2 + 5;
      iVar1 = iVar1 + 1;
    } while (iVar1 < DAT_1000b5e8);
  }
  HeapFree(DAT_1000b5f0,0,DAT_1000b5ec);
  HeapDestroy(DAT_1000b5f0);
  return;
}


