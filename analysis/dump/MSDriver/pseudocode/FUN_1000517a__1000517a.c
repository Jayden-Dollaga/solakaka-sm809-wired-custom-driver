// Program: MSDriver.dll
// Function: FUN_1000517a
// Entry: 1000517a
// Body: 1000517a - 100051a2
// Signature: undefined FUN_1000517a(void)


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1000517a(void)

{
  int iVar1;
  undefined4 *puVar2;
  
  puVar2 = &DAT_1000a380;
  for (iVar1 = 0x40; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0;
    puVar2 = puVar2 + 1;
  }
  *(undefined1 *)puVar2 = 0;
  DAT_1000a258 = 0;
  _DAT_1000a26c = 0;
  DAT_1000a484 = 0;
  DAT_1000a260 = 0;
  DAT_1000a264 = 0;
  DAT_1000a268 = 0;
  return;
}


