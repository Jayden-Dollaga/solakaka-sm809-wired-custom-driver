// Program: Hook.dll
// Function: FUN_1000321e
// Entry: 1000321e
// Body: 1000321e - 10003289
// Signature: undefined FUN_1000321e(void)


void FUN_1000321e(void)

{
  undefined **ppuVar1;
  
  ppuVar1 = (undefined **)&DAT_100075f0;
  do {
    if (((((LPCRITICAL_SECTION)*ppuVar1 != (LPCRITICAL_SECTION)0x0) &&
         (ppuVar1 != &PTR_DAT_10007634)) && (ppuVar1 != &PTR_DAT_10007624)) &&
       ((ppuVar1 != &PTR_DAT_10007614 && (ppuVar1 != &PTR_DAT_100075f4)))) {
      DeleteCriticalSection((LPCRITICAL_SECTION)*ppuVar1);
      FUN_1000338d(*ppuVar1);
    }
    ppuVar1 = ppuVar1 + 1;
  } while ((int)ppuVar1 < 0x100076b0);
  DeleteCriticalSection((LPCRITICAL_SECTION)PTR_DAT_10007614);
  DeleteCriticalSection((LPCRITICAL_SECTION)PTR_DAT_10007624);
  DeleteCriticalSection((LPCRITICAL_SECTION)PTR_DAT_10007634);
  DeleteCriticalSection((LPCRITICAL_SECTION)PTR_DAT_100075f4);
  return;
}


