// Program: Hook.dll
// Function: FUN_100048e4
// Entry: 100048e4
// Body: 100048e4 - 1000493f
// Signature: undefined4 FUN_100048e4(int * param_1)


undefined4 __cdecl FUN_100048e4(int *param_1)

{
  DWORD DVar1;
  undefined4 uVar2;
  DWORD DVar3;
  
  uVar2 = 0;
  if ((((byte)param_1[3] & 3) == 2) && ((param_1[3] & 0x108U) != 0)) {
    DVar3 = *param_1 - param_1[2];
    if (0 < (int)DVar3) {
      DVar1 = FUN_10002c04(param_1[4],(char *)param_1[2],DVar3);
      if (DVar1 == DVar3) {
        if ((param_1[3] & 0x80U) != 0) {
          param_1[3] = param_1[3] & 0xfffffffd;
        }
      }
      else {
        param_1[3] = param_1[3] | 0x20;
        uVar2 = 0xffffffff;
      }
    }
  }
  param_1[1] = 0;
  *param_1 = param_1[2];
  return uVar2;
}


