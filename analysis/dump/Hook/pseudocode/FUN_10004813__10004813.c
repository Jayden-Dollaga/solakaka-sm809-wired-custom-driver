// Program: Hook.dll
// Function: FUN_10004813
// Entry: 10004813
// Body: 10004813 - 10004834
// Signature: undefined FUN_10004813(uint param_1)


void __cdecl FUN_10004813(uint param_1)

{
  LeaveCriticalSection
            ((LPCRITICAL_SECTION)
             ((&DAT_10009300)[(int)param_1 >> 5] + 0xc + (param_1 & 0x1f) * 0x24));
  return;
}


