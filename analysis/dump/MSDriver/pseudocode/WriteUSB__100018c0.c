// Program: MSDriver.dll
// Function: WriteUSB
// Entry: 100018c0
// Body: 100018c0 - 100019c1
// Signature: bool WriteUSB(undefined4 * param_1, uint param_2)


bool __cdecl WriteUSB(undefined4 *param_1,uint param_2)

{
  HANDLE hHandle;
  BOOL BVar1;
  DWORD DVar2;
  int iVar3;
  uint uVar4;
  undefined4 *puVar5;
  DWORD local_7c;
  _OVERLAPPED local_78;
  undefined1 local_64;
  undefined4 local_63 [24];
  
                    /* 0x18c0  11  WriteUSB */
  if (DAT_10009ee0 != 0) {
    return false;
  }
  puVar5 = (undefined4 *)&local_64;
  for (iVar3 = 0x19; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar5 = 0;
    puVar5 = puVar5 + 1;
  }
  local_64 = 0;
  puVar5 = local_63;
  for (uVar4 = param_2 >> 2; uVar4 != 0; uVar4 = uVar4 - 1) {
    *puVar5 = *param_1;
    param_1 = param_1 + 1;
    puVar5 = puVar5 + 1;
  }
  for (uVar4 = param_2 & 3; uVar4 != 0; uVar4 = uVar4 - 1) {
    *(undefined1 *)puVar5 = *(undefined1 *)param_1;
    param_1 = (undefined4 *)((int)param_1 + 1);
    puVar5 = (undefined4 *)((int)puVar5 + 1);
  }
  hHandle = CreateEventA((LPSECURITY_ATTRIBUTES)0x0,1,0,(LPCSTR)0x0);
  local_78.Internal = 0;
  local_78.InternalHigh = 0;
  local_78.u.s.Offset = 0;
  local_78.u.s.OffsetHigh = 0;
  local_78.hEvent = hHandle;
  EnterCriticalSection((LPCRITICAL_SECTION)&DAT_10009e98);
  BVar1 = WriteFile(DAT_10009df4,&local_64,0x21,&local_7c,&local_78);
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
    return false;
  }
  return local_7c == 0x21;
}


