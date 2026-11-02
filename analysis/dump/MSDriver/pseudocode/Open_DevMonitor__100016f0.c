// Program: MSDriver.dll
// Function: Open_DevMonitor
// Entry: 100016f0
// Body: 100016f0 - 1000185c
// Signature: undefined4 Open_DevMonitor(undefined4 param_1, undefined4 param_2, undefined4 param_3)


undefined4 __cdecl Open_DevMonitor(undefined4 param_1,undefined4 param_2,undefined4 param_3)

{
  bool bVar1;
  DWORD DVar2;
  undefined3 extraout_var;
  _OSVERSIONINFOA local_94;
  
                    /* 0x16f0  5  Open_DevMonitor */
  DAT_10009ec8 = param_1;
  DAT_10009ec4 = param_3;
  DAT_10009ec0 = param_2;
  local_94.dwOSVersionInfoSize = 0x94;
  GetVersionExA(&local_94);
  DAT_10009edc = local_94.dwPlatformId;
  if (local_94.dwPlatformId == 2) {
    if (DAT_1000c00c != (HANDLE)0x0) {
      return 1;
    }
  }
  else if (((local_94.dwPlatformId != 1) || (DAT_10009ed0 != 0)) || (DAT_1000c00c != (HANDLE)0x0))
  goto LAB_10001847;
  DAT_10009ee4 = CreateEventA((LPSECURITY_ATTRIBUTES)0x0,0,0,(LPCSTR)0x0);
  DAT_1000c00c = CreateThread((LPSECURITY_ATTRIBUTES)0x0,0,(LPTHREAD_START_ROUTINE)&LAB_10001000,
                              (LPVOID)0x0,0,(LPDWORD)&DAT_1000c008);
  if (DAT_1000c00c == (HANDLE)0x0) {
    CloseHandle(DAT_10009ee4);
    return 0;
  }
  DVar2 = WaitForSingleObject(DAT_10009ee4,2000);
  if (DVar2 == 0x102) {
    CloseHandle(DAT_10009ee4);
    SendMessageA(DAT_1000c000,0x10,0,0);
    return 0;
  }
  CloseHandle(DAT_10009ee4);
  bVar1 = FUN_10001590((undefined4 *)&DAT_10009ed4);
  if (CONCAT31(extraout_var,bVar1) != 1) {
    if (DAT_1000c00c != (HANDLE)0x0) {
      SendMessageA(DAT_1000c000,0x10,0,0);
    }
    DAT_1000c00c = (HANDLE)0x0;
    return 0;
  }
LAB_10001847:
  FUN_10001df0((undefined4 *)0x0);
  return 1;
}


