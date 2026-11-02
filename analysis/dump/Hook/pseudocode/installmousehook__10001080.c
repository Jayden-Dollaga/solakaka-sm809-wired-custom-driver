// Program: Hook.dll
// Function: installmousehook
// Entry: 10001080
// Body: 10001080 - 100010b7
// Signature: bool installmousehook(undefined4 param_1)


bool __cdecl installmousehook(undefined4 param_1)

{
                    /* 0x1080  6  installmousehook */
  DAT_1000a008 = (HHOOK)0x0;
  DAT_1000a00c = param_1;
  DAT_1000a008 = SetWindowsHookExA(0xe,mousehookproc,DAT_10007d18,0);
  return DAT_1000a008 != (HHOOK)0x0;
}


