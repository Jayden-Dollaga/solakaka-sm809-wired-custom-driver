// Program: SM809 mouse Software.exe
// Function: FUN_00414910
// Entry: 00414910
// Body: 00414910 - 00414979
// Signature: undefined4 FUN_00414910(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

undefined4 FUN_00414910(int param_1)

{
  int iVar1;
  tagMSG local_24;
  undefined4 local_8;
  
  local_8 = DAT_00432008 ^ (int)register0x00000010 - 4U;
  iVar1 = GetMessageW(&local_24,(HWND)0x0,0,0);
  while (iVar1 != 0) {
    if ((local_24.message == 0x670) && (local_24.wParam == 0)) {
      FUN_00418a40(param_1);
    }
    iVar1 = GetMessageW(&local_24,(HWND)0x0,0,0);
  }
  return 0;
}


