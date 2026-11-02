// Program: Hook.dll
// Function: MouseMoveHook
// Entry: 10001100
// Body: 10001100 - 1000110e
// Signature: undefined4 MouseMoveHook(undefined4 param_1)


undefined4 __cdecl MouseMoveHook(undefined4 param_1)

{
                    /* 0x1100  1  MouseMoveHook */
  DAT_10007d24 = param_1;
  return 1;
}


