// Program: MSDriver.dll
// Function: ReadUSB
// Entry: 100019d0
// Body: 100019d0 - 10001acd
// Signature: undefined4 ReadUSB(undefined4 * param_1)


undefined4 __cdecl ReadUSB(undefined4 *param_1)

{
  HANDLE hHandle;
  BOOL BVar1;
  DWORD DVar2;
  int iVar3;
  undefined4 *puVar4;
  DWORD local_7c;
  _OVERLAPPED local_78;
  undefined1 local_64;
  undefined4 local_63 [24];
  
                    /* 0x19d0  8  ReadUSB */
  if (DAT_10009ee0 != 0) {
    return 0;
  }
  puVar4 = (undefined4 *)&local_64;
  for (iVar3 = 0x19; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0;
    puVar4 = puVar4 + 1;
  }
  local_64 = 0;
  hHandle = CreateEventA((LPSECURITY_ATTRIBUTES)0x0,1,0,(LPCSTR)0x0);
  local_78.Internal = 0;
  local_78.InternalHigh = 0;
  local_78.u.s.Offset = 0;
  local_78.u.s.OffsetHigh = 0;
  local_78.hEvent = hHandle;
  EnterCriticalSection((LPCRITICAL_SECTION)&DAT_10009e98);
  BVar1 = ReadFile(DAT_10009df4,&local_64,0x21,&local_7c,&local_78);
  LeaveCriticalSection((LPCRITICAL_SECTION)&DAT_10009e98);
  if (BVar1 == 0) {
    DVar2 = GetLastError();
    if (DVar2 == 0x3e5) {
      WaitForSingleObject(hHandle,2000);
      GetOverlappedResult(DAT_10009df4,&local_78,&local_7c,0);
      BVar1 = 1;
    }
  }
  CloseHandle(hHandle);
  if (BVar1 == 0) {
    return 0;
  }
  if (local_7c != 0x21) {
    return 0;
  }
  puVar4 = local_63;
  for (iVar3 = 8; iVar3 != 0; iVar3 = iVar3 + -1) {
    *param_1 = *puVar4;
    puVar4 = puVar4 + 1;
    param_1 = param_1 + 1;
  }
  *(undefined1 *)param_1 = *(undefined1 *)puVar4;
  return 1;
}


