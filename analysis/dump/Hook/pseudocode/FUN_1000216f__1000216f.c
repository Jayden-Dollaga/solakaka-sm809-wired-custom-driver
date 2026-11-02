// Program: Hook.dll
// Function: FUN_1000216f
// Entry: 1000216f
// Body: 1000216f - 1000218c
// Signature: undefined FUN_1000216f(void)


void FUN_1000216f(void)

{
  FUN_1000321e();
  if (DAT_10007080 != 0xffffffff) {
    TlsFree(DAT_10007080);
    DAT_10007080 = 0xffffffff;
  }
  return;
}


