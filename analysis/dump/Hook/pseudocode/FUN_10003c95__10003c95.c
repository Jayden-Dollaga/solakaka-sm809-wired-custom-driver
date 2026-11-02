// Program: Hook.dll
// Function: FUN_10003c95
// Entry: 10003c95
// Body: 10003c95 - 10003cd2
// Signature: undefined4 FUN_10003c95(void)


undefined4 FUN_10003c95(void)

{
  DAT_1000809c = HeapAlloc(DAT_100092e4,0,0x140);
  if (DAT_1000809c == (LPVOID)0x0) {
    return 0;
  }
  DAT_10008094 = 0;
  DAT_10008098 = 0;
  DAT_10008090 = DAT_1000809c;
  DAT_10008088 = 0x10;
  return 1;
}


