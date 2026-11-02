// Program: Hook.dll
// Function: FUN_1000378a
// Entry: 1000378a
// Body: 1000378a - 100037b2
// Signature: undefined FUN_1000378a(void)


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1000378a(void)

{
  int iVar1;
  undefined4 *puVar2;
  
  puVar2 = &DAT_100081c0;
  for (iVar1 = 0x40; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0;
    puVar2 = puVar2 + 1;
  }
  *(undefined1 *)puVar2 = 0;
  DAT_100080a0 = 0;
  _DAT_100080bc = 0;
  DAT_100082c4 = 0;
  DAT_100080b0 = 0;
  DAT_100080b4 = 0;
  DAT_100080b8 = 0;
  return;
}


