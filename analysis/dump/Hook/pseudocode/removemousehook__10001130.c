// Program: Hook.dll
// Function: removemousehook
// Entry: 10001130
// Body: 10001130 - 10001141
// Signature: undefined4 removemousehook(void)


undefined4 removemousehook(void)

{
                    /* 0x1130  9  removemousehook */
  UnhookWindowsHookEx(DAT_1000a008);
  return 1;
}


