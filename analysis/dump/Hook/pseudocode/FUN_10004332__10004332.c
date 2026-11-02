// Program: Hook.dll
// Function: FUN_10004332
// Entry: 10004332
// Body: 10004332 - 100043e2
// Signature: undefined4 * FUN_10004332(void)


undefined4 * FUN_10004332(void)

{
  undefined4 *puVar1;
  LPVOID pvVar2;
  
  if (DAT_10008098 == DAT_10008088) {
    pvVar2 = HeapReAlloc(DAT_100092e4,0,DAT_1000809c,(DAT_10008088 * 5 + 0x50) * 4);
    if (pvVar2 == (LPVOID)0x0) {
      return (undefined4 *)0x0;
    }
    DAT_10008088 = DAT_10008088 + 0x10;
    DAT_1000809c = pvVar2;
  }
  puVar1 = (undefined4 *)((int)DAT_1000809c + DAT_10008098 * 0x14);
  pvVar2 = HeapAlloc(DAT_100092e4,8,0x41c4);
  puVar1[4] = pvVar2;
  if (pvVar2 != (LPVOID)0x0) {
    pvVar2 = VirtualAlloc((LPVOID)0x0,0x100000,0x2000,4);
    puVar1[3] = pvVar2;
    if (pvVar2 != (LPVOID)0x0) {
      puVar1[2] = 0xffffffff;
      *puVar1 = 0;
      puVar1[1] = 0;
      DAT_10008098 = DAT_10008098 + 1;
      *(undefined4 *)puVar1[4] = 0xffffffff;
      return puVar1;
    }
    HeapFree(DAT_100092e4,0,(LPVOID)puVar1[4]);
  }
  return (undefined4 *)0x0;
}


