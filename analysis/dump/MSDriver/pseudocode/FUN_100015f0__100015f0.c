// Program: MSDriver.dll
// Function: FUN_100015f0
// Entry: 100015f0
// Body: 100015f0 - 10001603
// Signature: bool FUN_100015f0(undefined4 * param_1)


bool __cdecl FUN_100015f0(undefined4 *param_1)

{
  BOOL BVar1;
  
  BVar1 = UnregisterDeviceNotification((HDEVNOTIFY)*param_1);
  return BVar1 != 0;
}


