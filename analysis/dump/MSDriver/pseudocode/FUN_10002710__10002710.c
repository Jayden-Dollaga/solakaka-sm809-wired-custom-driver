// Program: MSDriver.dll
// Function: FUN_10002710
// Entry: 10002710
// Body: 10002710 - 1000277b
// Signature: undefined FUN_10002710(void)


void FUN_10002710(void)

{
  undefined **ppuVar1;
  
  ppuVar1 = (undefined **)&DAT_1000914c;
  do {
    if (((((LPCRITICAL_SECTION)*ppuVar1 != (LPCRITICAL_SECTION)0x0) &&
         (ppuVar1 != &PTR_DAT_10009190)) && (ppuVar1 != &PTR_DAT_10009180)) &&
       ((ppuVar1 != &PTR_DAT_10009170 && (ppuVar1 != &PTR_DAT_10009150)))) {
      DeleteCriticalSection((LPCRITICAL_SECTION)*ppuVar1);
      FUN_100022da(*ppuVar1);
    }
    ppuVar1 = ppuVar1 + 1;
  } while ((int)ppuVar1 < 0x1000920c);
  DeleteCriticalSection((LPCRITICAL_SECTION)PTR_DAT_10009170);
  DeleteCriticalSection((LPCRITICAL_SECTION)PTR_DAT_10009180);
  DeleteCriticalSection((LPCRITICAL_SECTION)PTR_DAT_10009190);
  DeleteCriticalSection((LPCRITICAL_SECTION)PTR_DAT_10009150);
  return;
}


