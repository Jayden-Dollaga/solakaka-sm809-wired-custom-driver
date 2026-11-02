// Program: MSDriver.dll
// Function: FUN_10002e8f
// Entry: 10002e8f
// Body: 10002e8f - 10002f3f
// Signature: undefined4 * FUN_10002e8f(void)


undefined4 * FUN_10002e8f(void)

{
  undefined4 *puVar1;
  LPVOID pvVar2;
  
  if (DAT_1000b5e8 == DAT_1000b5d8) {
    pvVar2 = HeapReAlloc(DAT_1000b5f0,0,DAT_1000b5ec,(DAT_1000b5d8 * 5 + 0x50) * 4);
    if (pvVar2 == (LPVOID)0x0) {
      return (undefined4 *)0x0;
    }
    DAT_1000b5d8 = DAT_1000b5d8 + 0x10;
    DAT_1000b5ec = pvVar2;
  }
  puVar1 = (undefined4 *)((int)DAT_1000b5ec + DAT_1000b5e8 * 0x14);
  pvVar2 = HeapAlloc(DAT_1000b5f0,8,0x41c4);
  puVar1[4] = pvVar2;
  if (pvVar2 != (LPVOID)0x0) {
    pvVar2 = VirtualAlloc((LPVOID)0x0,0x100000,0x2000,4);
    puVar1[3] = pvVar2;
    if (pvVar2 != (LPVOID)0x0) {
      puVar1[2] = 0xffffffff;
      *puVar1 = 0;
      puVar1[1] = 0;
      DAT_1000b5e8 = DAT_1000b5e8 + 1;
      *(undefined4 *)puVar1[4] = 0xffffffff;
      return puVar1;
    }
    HeapFree(DAT_1000b5f0,0,(LPVOID)puVar1[4]);
  }
  return (undefined4 *)0x0;
}


