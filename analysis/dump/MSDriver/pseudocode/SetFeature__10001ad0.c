// Program: MSDriver.dll
// Function: SetFeature
// Entry: 10001ad0
// Body: 10001ad0 - 10001b28
// Signature: undefined1 SetFeature(undefined4 * param_1, uint param_2)


undefined1 __cdecl SetFeature(undefined4 *param_1,uint param_2)

{
  undefined1 uVar1;
  int iVar2;
  uint uVar3;
  undefined4 *puVar4;
  undefined1 local_64;
  undefined4 local_63 [24];
  
  puVar4 = (undefined4 *)&local_64;
                    /* 0x1ad0  9  SetFeature */
  for (iVar2 = 0x19; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0;
    puVar4 = puVar4 + 1;
  }
  local_64 = 0;
  puVar4 = local_63;
  for (uVar3 = param_2 >> 2; uVar3 != 0; uVar3 = uVar3 - 1) {
    *puVar4 = *param_1;
    param_1 = param_1 + 1;
    puVar4 = puVar4 + 1;
  }
  for (uVar3 = param_2 & 3; uVar3 != 0; uVar3 = uVar3 - 1) {
    *(undefined1 *)puVar4 = *(undefined1 *)param_1;
    param_1 = (undefined4 *)((int)param_1 + 1);
    puVar4 = (undefined4 *)((int)puVar4 + 1);
  }
  if (DAT_10009df4 == 0) {
    return 0;
  }
  uVar1 = HidD_SetFeature(DAT_10009df4,&local_64,9);
  return uVar1;
}


