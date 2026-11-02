// Program: MSDriver.dll
// Function: GetFeature
// Entry: 10001b30
// Body: 10001b30 - 10001b89
// Signature: undefined1 GetFeature(undefined4 * param_1, uint param_2)


undefined1 __cdecl GetFeature(undefined4 *param_1,uint param_2)

{
  undefined1 uVar1;
  int iVar2;
  uint uVar3;
  undefined4 *puVar4;
  undefined1 local_64;
  undefined4 local_63 [24];
  
                    /* 0x1b30  4  GetFeature */
  puVar4 = (undefined4 *)&local_64;
  for (iVar2 = 0x19; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0;
    puVar4 = puVar4 + 1;
  }
  local_64 = 0;
  if (DAT_10009df4 == 0) {
    return 0;
  }
  uVar1 = HidD_GetFeature(DAT_10009df4,&local_64,9);
  puVar4 = local_63;
  for (uVar3 = param_2 >> 2; uVar3 != 0; uVar3 = uVar3 - 1) {
    *param_1 = *puVar4;
    puVar4 = puVar4 + 1;
    param_1 = param_1 + 1;
  }
  for (uVar3 = param_2 & 3; uVar3 != 0; uVar3 = uVar3 - 1) {
    *(undefined1 *)param_1 = *(undefined1 *)puVar4;
    puVar4 = (undefined4 *)((int)puVar4 + 1);
    param_1 = (undefined4 *)((int)param_1 + 1);
  }
  return uVar1;
}


