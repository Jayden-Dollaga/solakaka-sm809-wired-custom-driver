// Program: MSDriver.dll
// Function: FUN_10003b47
// Entry: 10003b47
// Body: 10003b47 - 10003b64
// Signature: undefined FUN_10003b47(void)


void FUN_10003b47(void)

{
  FUN_10002710();
  if (DAT_10009218 != 0xffffffff) {
    TlsFree(DAT_10009218);
    DAT_10009218 = 0xffffffff;
  }
  return;
}


