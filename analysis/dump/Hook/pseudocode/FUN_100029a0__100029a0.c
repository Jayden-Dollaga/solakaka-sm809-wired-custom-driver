// Program: Hook.dll
// Function: FUN_100029a0
// Entry: 100029a0
// Body: 100029a0 - 100029d8
// Signature: undefined FUN_100029a0(void)


void FUN_100029a0(void)

{
  if ((DAT_10007d3c == 1) || ((DAT_10007d3c == 0 && (DAT_10007d40 == 1)))) {
    FUN_100029d9(0xfc);
    if (DAT_10007e90 != (code *)0x0) {
      (*DAT_10007e90)();
    }
    FUN_100029d9(0xff);
  }
  return;
}


