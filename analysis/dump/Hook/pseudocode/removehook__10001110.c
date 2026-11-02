// Program: Hook.dll
// Function: removehook
// Entry: 10001110
// Body: 10001110 - 10001121
// Signature: undefined4 removehook(void)


undefined4 removehook(void)

{
                    /* 0x1110  8  removehook */
  UnhookWindowsHookEx(DAT_1000a000);
  return 1;
}


