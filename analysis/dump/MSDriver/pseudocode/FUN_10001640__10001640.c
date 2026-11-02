// Program: MSDriver.dll
// Function: FUN_10001640
// Entry: 10001640
// Body: 10001640 - 100016c0
// Signature: undefined4 FUN_10001640(int param_1)


undefined4 __cdecl FUN_10001640(int param_1)

{
  BOOL BVar1;
  DWORD local_4;
  
  local_4 = 0;
  if (*(HANDLE *)(param_1 + 0xa4) != (HANDLE)0x0) {
    GetExitCodeThread(*(HANDLE *)(param_1 + 0xa4),&local_4);
    BVar1 = TerminateThread(*(HANDLE *)(param_1 + 0xa4),local_4);
    if (BVar1 == 0) {
      Sleep(100);
      GetExitCodeThread(*(HANDLE *)(param_1 + 0xa4),&local_4);
      BVar1 = TerminateThread(*(HANDLE *)(param_1 + 0xa4),local_4);
      if (BVar1 == 0) {
        return 0;
      }
    }
    *(undefined4 *)(param_1 + 0xa4) = 0;
  }
  return 1;
}


