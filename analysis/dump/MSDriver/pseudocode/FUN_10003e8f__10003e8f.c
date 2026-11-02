// Program: MSDriver.dll
// Function: FUN_10003e8f
// Entry: 10003e8f
// Body: 10003e8f - 10003f47
// Signature: undefined FUN_10003e8f(void)


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_10003e8f(void)

{
  char cVar1;
  size_t sVar2;
  undefined4 *puVar3;
  void *pvVar4;
  int iVar5;
  uint *puVar6;
  
  if (DAT_1000b5c8 == 0) {
    FUN_10005328();
  }
  iVar5 = 0;
  for (puVar6 = DAT_10009f00; (char)*puVar6 != '\0'; puVar6 = (uint *)((int)puVar6 + sVar2 + 1)) {
    if ((char)*puVar6 != '=') {
      iVar5 = iVar5 + 1;
    }
    sVar2 = _strlen((char *)puVar6);
  }
  puVar3 = _malloc(iVar5 * 4 + 4);
  _DAT_10009f98 = puVar3;
  if (puVar3 == (undefined4 *)0x0) {
    __amsg_exit(9);
  }
  cVar1 = (char)*DAT_10009f00;
  puVar6 = DAT_10009f00;
  while (cVar1 != '\0') {
    sVar2 = _strlen((char *)puVar6);
    if ((char)*puVar6 != '=') {
      pvVar4 = _malloc(sVar2 + 1);
      *puVar3 = pvVar4;
      if (pvVar4 == (void *)0x0) {
        __amsg_exit(9);
      }
      FUN_10004e60((uint *)*puVar3,puVar6);
      puVar3 = puVar3 + 1;
    }
    puVar6 = (uint *)((int)puVar6 + sVar2 + 1);
    cVar1 = (char)*puVar6;
  }
  FUN_100022da(DAT_10009f00);
  DAT_10009f00 = (uint *)0x0;
  *puVar3 = 0;
  _DAT_1000b5c4 = 1;
  return;
}


