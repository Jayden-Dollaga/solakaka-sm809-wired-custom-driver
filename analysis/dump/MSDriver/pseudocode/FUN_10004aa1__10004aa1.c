// Program: MSDriver.dll
// Function: FUN_10004aa1
// Entry: 10004aa1
// Body: 10004aa1 - 10004ac9
// Signature: byte FUN_10004aa1(uint param_1)


byte __cdecl FUN_10004aa1(uint param_1)

{
  if (param_1 < DAT_1000b5c0) {
    return *(byte *)((&DAT_1000b4c0)[(int)param_1 >> 5] + 4 + (param_1 & 0x1f) * 0x24) & 0x40;
  }
  return 0;
}


