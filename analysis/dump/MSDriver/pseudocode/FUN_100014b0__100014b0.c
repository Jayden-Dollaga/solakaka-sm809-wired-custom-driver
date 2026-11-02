// Program: MSDriver.dll
// Function: FUN_100014b0
// Entry: 100014b0
// Body: 100014b0 - 1000158c
// Signature: undefined4 FUN_100014b0(undefined4 * param_1)


undefined4 __cdecl FUN_100014b0(undefined4 *param_1)

{
  HDEVNOTIFY pvVar1;
  HANDLE pvVar2;
  undefined4 local_2c;
  undefined4 local_28;
  undefined4 local_20;
  
  local_20 = param_1[3];
  param_1[0x28] = 0;
  local_2c = 0x2c;
  local_28 = 6;
  pvVar1 = RegisterDeviceNotificationA(DAT_1000c000,&local_2c,0);
  param_1[0x28] = pvVar1;
  if (pvVar1 == (HDEVNOTIFY)0x0) {
    return 0;
  }
  pvVar2 = CreateThread((LPSECURITY_ATTRIBUTES)0x0,0,(LPTHREAD_START_ROUTINE)&DAT_10001610,param_1,0
                        ,param_1 + 0x2a);
  param_1[0x29] = pvVar2;
  if (pvVar2 == (HANDLE)0x0) {
    FUN_10001f90(param_1 + 3);
    FUN_100022da(param_1);
    return 0;
  }
  *(undefined2 *)(param_1 + 2) = (undefined2)DAT_10009030;
  DAT_10009030 = DAT_10009030 + 1;
  FUN_10001470(1,CONCAT22((short)((uint)DAT_10009030 >> 0x10),*(undefined2 *)(param_1 + 2)));
  *param_1 = &DAT_10009eb8;
  param_1[1] = DAT_10009ebc;
  *DAT_10009ebc = param_1;
  DAT_10009ebc = param_1;
  return 1;
}


