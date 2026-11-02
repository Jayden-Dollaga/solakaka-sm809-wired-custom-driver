// Program: Hook.dll
// Function: enablemousehook
// Entry: 100010c0
// Body: 100010c0 - 100010d3
// Signature: undefined4 enablemousehook(uint param_1)


undefined4 __cdecl enablemousehook(uint param_1)

{
                    /* 0x10c0  3  enablemousehook */
  DAT_10007d20 = param_1 & 0xff;
  return 1;
}


