// Program: MSDriver.dll
// Function: FUN_100042c7
// Entry: 100042c7
// Body: 100042c7 - 100042ff
// Signature: undefined FUN_100042c7(void)


void FUN_100042c7(void)

{
  if ((DAT_10009f08 == 1) || ((DAT_10009f08 == 0 && (DAT_10009f0c == 1)))) {
    FUN_10004300(0xfc);
    if (DAT_1000a0c4 != (code *)0x0) {
      (*DAT_1000a0c4)();
    }
    FUN_10004300(0xff);
  }
  return;
}


