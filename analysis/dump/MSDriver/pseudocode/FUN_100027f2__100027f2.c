// Program: MSDriver.dll
// Function: FUN_100027f2
// Entry: 100027f2
// Body: 100027f2 - 1000282f
// Signature: undefined4 FUN_100027f2(void)


undefined4 FUN_100027f2(void)

{
  DAT_1000b5ec = HeapAlloc(DAT_1000b5f0,0,0x140);
  if (DAT_1000b5ec == (LPVOID)0x0) {
    return 0;
  }
  DAT_1000b5e4 = 0;
  DAT_1000b5e8 = 0;
  DAT_1000b5e0 = DAT_1000b5ec;
  DAT_1000b5d8 = 0x10;
  return 1;
}


