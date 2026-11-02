// Program: MSDriver.dll
// Function: FUN_10001590
// Entry: 10001590
// Body: 10001590 - 100015e6
// Signature: bool FUN_10001590(undefined4 * param_1)


bool __cdecl FUN_10001590(undefined4 *param_1)

{
  HDEVNOTIFY pvVar1;
  undefined4 local_20;
  undefined4 local_1c;
  undefined1 local_14 [20];
  
  if (param_1 == (undefined4 *)0x0) {
    return false;
  }
  *param_1 = 0;
  local_20 = 0x20;
  local_1c = 5;
  HidD_GetHidGuid(local_14);
  pvVar1 = RegisterDeviceNotificationA(DAT_1000c000,&local_20,0);
  *param_1 = pvVar1;
  return pvVar1 != (HDEVNOTIFY)0x0;
}


