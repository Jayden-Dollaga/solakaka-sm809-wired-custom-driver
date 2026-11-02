// Program: MSDriver.dll
// Function: FUN_100059b3
// Entry: 100059b3
// Body: 100059b3 - 100059d4
// Signature: undefined FUN_100059b3(uint param_1)


void __cdecl FUN_100059b3(uint param_1)

{
  LeaveCriticalSection
            ((LPCRITICAL_SECTION)
             ((&DAT_1000b4c0)[(int)param_1 >> 5] + 0xc + (param_1 & 0x1f) * 0x24));
  return;
}


