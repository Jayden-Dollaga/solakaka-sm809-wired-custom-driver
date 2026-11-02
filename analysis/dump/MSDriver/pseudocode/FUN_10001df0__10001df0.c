// Program: MSDriver.dll
// Function: FUN_10001df0
// Entry: 10001df0
// Body: 10001df0 - 10001f87
// Signature: uint FUN_10001df0(undefined4 * param_1)


uint __cdecl FUN_10001df0(undefined4 *param_1)

{
  HDEVINFO DeviceInfoSet;
  DWORD DVar1;
  PSP_DEVICE_INTERFACE_DETAIL_DATA_A DeviceInterfaceDetailData;
  BOOL BVar2;
  undefined4 *puVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 *puVar6;
  uint local_38;
  DWORD local_34;
  DWORD local_30;
  GUID local_2c;
  _SP_DEVICE_INTERFACE_DATA local_1c;
  
  local_34 = 0;
  HidD_GetHidGuid(&local_2c);
  DeviceInfoSet = SetupDiGetClassDevsA(&local_2c,(PCSTR)0x0,(HWND)0x0,0x12);
  local_1c.cbSize = 0x1c;
  local_30 = 0;
  local_38 = 0;
  puVar3 = param_1;
  do {
    while( true ) {
      DVar1 = local_30;
      local_30 = local_30 + 1;
      SetupDiEnumDeviceInterfaces(DeviceInfoSet,(PSP_DEVINFO_DATA)0x0,&local_2c,DVar1,&local_1c);
      DVar1 = GetLastError();
      if (DVar1 == 0x103) goto LAB_10001f56;
      SetupDiGetDeviceInterfaceDetailA
                (DeviceInfoSet,&local_1c,(PSP_DEVICE_INTERFACE_DETAIL_DATA_A)0x0,0,&local_34,
                 (PSP_DEVINFO_DATA)0x0);
      DVar1 = local_34;
      DeviceInterfaceDetailData = _malloc(local_34);
      DeviceInterfaceDetailData->cbSize = 5;
      BVar2 = SetupDiGetDeviceInterfaceDetailA
                        (DeviceInfoSet,&local_1c,DeviceInterfaceDetailData,DVar1,&local_34,
                         (PSP_DEVINFO_DATA)0x0);
      if (BVar2 != 0) {
        puVar3 = _malloc(0xac);
        puVar5 = puVar3;
        for (iVar4 = 0x2b; iVar4 != 0; iVar4 = iVar4 + -1) {
          *puVar5 = 0;
          puVar5 = puVar5 + 1;
        }
        if (puVar3 == (undefined4 *)0x0) {
          local_38 = 0;
          goto LAB_10001f56;
        }
        local_38 = FUN_10001c00(DeviceInterfaceDetailData->DevicePath,puVar3 + 3,(int)param_1);
        local_38 = local_38 & 0xff;
      }
      FUN_100022da(DeviceInterfaceDetailData);
      if (local_38 == 1) break;
LAB_10001f18:
      FUN_100022da(puVar3);
    }
    if (param_1 != (undefined4 *)0x0) {
      if (param_1 == (undefined4 *)0x1) {
        FUN_100022da(puVar3);
      }
      else {
        if (param_1 != (undefined4 *)0x2) goto LAB_10001f18;
        puVar5 = puVar3;
        puVar6 = &DAT_10009de8;
        for (iVar4 = 0x2b; iVar4 != 0; iVar4 = iVar4 + -1) {
          *puVar6 = *puVar5;
          puVar5 = puVar5 + 1;
          puVar6 = puVar6 + 1;
        }
        FUN_100022da(puVar3);
      }
      break;
    }
    iVar4 = FUN_100014b0(puVar3);
  } while (iVar4 == 1);
LAB_10001f56:
  SetupDiDestroyDeviceInfoList(DeviceInfoSet);
  if (param_1 == (undefined4 *)0x0) {
    return -(uint)(DAT_10009030 != 1) & DAT_10009030;
  }
  return (uint)(local_38 == 1);
}


