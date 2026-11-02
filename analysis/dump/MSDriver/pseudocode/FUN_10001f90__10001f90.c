// Program: MSDriver.dll
// Function: FUN_10001f90
// Entry: 10001f90
// Body: 10001f90 - 10002088
// Signature: undefined4 FUN_10001f90(undefined4 * param_1)


uint __cdecl FUN_10001f90(undefined4 *param_1)

{
  HANDLE hObject;
  uint in_EAX;
  undefined4 uVar1;
  
  if (param_1 == (undefined4 *)0x0) {
    return in_EAX & 0xffffff00;
  }
  hObject = (HANDLE)*param_1;
  if ((hObject != (HANDLE)0xffffffff) && (hObject != (HANDLE)0x0)) {
    CloseHandle(hObject);
  }
  if (param_1[1] != 0) {
    HidD_FreePreparsedData(param_1[1]);
  }
  if ((LPVOID)param_1[0x15] != (LPVOID)0x0) {
    FUN_100022da((LPVOID)param_1[0x15]);
  }
  if ((LPVOID)param_1[0x16] != (LPVOID)0x0) {
    FUN_100022da((LPVOID)param_1[0x16]);
  }
  if ((LPVOID)param_1[0x18] != (LPVOID)0x0) {
    FUN_100022da((LPVOID)param_1[0x18]);
  }
  if ((LPVOID)param_1[0x19] != (LPVOID)0x0) {
    FUN_100022da((LPVOID)param_1[0x19]);
  }
  if ((LPVOID)param_1[0x1a] != (LPVOID)0x0) {
    FUN_100022da((LPVOID)param_1[0x1a]);
  }
  if ((LPVOID)param_1[0x1b] != (LPVOID)0x0) {
    FUN_100022da((LPVOID)param_1[0x1b]);
  }
  if ((LPVOID)param_1[0x1d] != (LPVOID)0x0) {
    FUN_100022da((LPVOID)param_1[0x1d]);
  }
  if ((LPVOID)param_1[0x1e] != (LPVOID)0x0) {
    FUN_100022da((LPVOID)param_1[0x1e]);
  }
  if ((LPVOID)param_1[0x1f] != (LPVOID)0x0) {
    FUN_100022da((LPVOID)param_1[0x1f]);
  }
  if ((LPVOID)param_1[0x20] != (LPVOID)0x0) {
    FUN_100022da((LPVOID)param_1[0x20]);
  }
  uVar1 = 0;
  if ((LPVOID)param_1[0x22] != (LPVOID)0x0) {
    uVar1 = FUN_100022da((LPVOID)param_1[0x22]);
  }
  if ((LPVOID)param_1[0x23] != (LPVOID)0x0) {
    uVar1 = FUN_100022da((LPVOID)param_1[0x23]);
  }
  return CONCAT31((int3)((uint)uVar1 >> 8),1);
}


