// Program: Hook.dll
// Function: FUN_100014e0
// Entry: 100014e0
// Body: 100014e0 - 10001531
// Signature: int FUN_100014e0(undefined1 * param_1, byte * param_2, undefined4 param_3)


int __cdecl FUN_100014e0(undefined1 *param_1,byte *param_2,undefined4 param_3)

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
  iVar1 = FUN_100017f3((int *)&local_24,param_2,&param_3);
  local_20 = local_20 + -1;
  if (local_20 < 0) {
    FUN_100016db(0,(int *)&local_24);
  }
  else {
    *local_24 = 0;
  }
  return iVar1;
}


