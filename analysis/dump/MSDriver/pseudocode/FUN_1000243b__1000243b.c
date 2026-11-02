// Program: MSDriver.dll
// Function: FUN_1000243b
// Entry: 1000243b
// Body: 1000243b - 1000248c
// Signature: int FUN_1000243b(undefined1 * param_1, byte * param_2, undefined4 param_3)


int __cdecl FUN_1000243b(undefined1 *param_1,byte *param_2,undefined4 param_3)

{
  int iVar1;
  undefined1 *local_24;
  int local_20;
  undefined1 *local_1c;
  undefined4 local_18;
  
  local_1c = param_1;
  local_24 = param_1;
  local_18 = 0x42;
  local_20 = 0x7fffffff;
  iVar1 = FUN_100031cb((int *)&local_24,param_2,&param_3);
  local_20 = local_20 + -1;
  if (local_20 < 0) {
    FUN_100030b3(0,(int *)&local_24);
  }
  else {
    *local_24 = 0;
  }
  return iVar1;
}


