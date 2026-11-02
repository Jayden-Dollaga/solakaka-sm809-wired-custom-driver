// Program: MSDriver.dll
// Function: entry
// Entry: 10002566
// Body: 10002566 - 10002602
// Signature: int entry(undefined4 param_1, int param_2, undefined4 param_3)


int entry(undefined4 param_1,int param_2,undefined4 param_3)

{
  int iVar1;
  int iVar2;
  int iVar3;
  
  iVar1 = param_2;
  if (param_2 == 0) {
    iVar2 = DAT_10009efc;
  }
  else {
    if ((param_2 != 1) && (param_2 != 2)) goto LAB_100025ae;
    if ((DAT_1000b5f8 != (code *)0x0) &&
       (iVar2 = (*DAT_1000b5f8)(param_1,param_2,param_3), iVar2 == 0)) {
      return 0;
    }
    iVar2 = FUN_1000248d(param_1,param_2);
  }
  if (iVar2 == 0) {
    return 0;
  }
LAB_100025ae:
  iVar2 = FUN_100010f0(param_1,param_2);
  if (param_2 == 1) {
    if (iVar2 != 0) {
      return iVar2;
    }
    FUN_1000248d(param_1,0);
  }
  if ((param_2 == 0) || (param_2 == 3)) {
    iVar3 = FUN_1000248d(param_1,param_2);
    param_2 = iVar2;
    if (iVar3 == 0) {
      param_2 = 0;
    }
    iVar2 = param_2;
    if ((param_2 != 0) && (DAT_1000b5f8 != (code *)0x0)) {
      iVar2 = (*DAT_1000b5f8)(param_1,iVar1,param_3);
    }
  }
  param_2 = iVar2;
  return param_2;
}


