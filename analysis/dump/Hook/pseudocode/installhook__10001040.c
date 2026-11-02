// Program: Hook.dll
// Function: installhook
// Entry: 10001040
// Body: 10001040 - 10001077
// Signature: bool installhook(undefined4 param_1)


bool __cdecl installhook(undefined4 param_1)

{
                    /* 0x1040  5  installhook */
  DAT_1000a000 = (HHOOK)0x0;
  DAT_1000a004 = param_1;
  DAT_1000a000 = SetWindowsHookExA(0xd,hookproc,DAT_10007d18,0);
  return DAT_1000a000 != (HHOOK)0x0;
}


