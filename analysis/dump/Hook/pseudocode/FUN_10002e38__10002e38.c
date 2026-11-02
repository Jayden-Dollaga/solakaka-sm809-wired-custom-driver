// Program: Hook.dll
// Function: FUN_10002e38
// Entry: 10002e38
// Body: 10002e38 - 10002e60
// Signature: byte FUN_10002e38(uint param_1)


byte __cdecl FUN_10002e38(uint param_1)

{
  if (param_1 < DAT_10009400) {
    return *(byte *)((&DAT_10009300)[(int)param_1 >> 5] + 4 + (param_1 & 0x1f) * 0x24) & 0x40;
  }
  return 0;
}


