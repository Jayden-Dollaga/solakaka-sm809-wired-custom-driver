// Program: MSDriver.dll
// Function: FUN_10003a22
// Entry: 10003a22
// Body: 10003a22 - 10003ac4
// Signature: undefined FUN_10003a22(UINT param_1, int param_2, int param_3)


void __cdecl FUN_10003a22(UINT param_1,int param_2,int param_3)

{
  HANDLE hProcess;
  undefined4 *puVar1;
  UINT uExitCode;
  
  FUN_10003ac7();
  if (DAT_10009fb8 == 1) {
    uExitCode = param_1;
    hProcess = GetCurrentProcess();
    TerminateProcess(hProcess,uExitCode);
  }
  DAT_10009fb4 = 1;
  DAT_10009fb0 = (undefined1)param_3;
  if (param_2 == 0) {
    if ((DAT_1000b5d0 != (undefined4 *)0x0) &&
       (puVar1 = (undefined4 *)(DAT_1000b5cc - 4), DAT_1000b5d0 <= puVar1)) {
      do {
        if ((code *)*puVar1 != (code *)0x0) {
          (*(code *)*puVar1)();
        }
        puVar1 = puVar1 + -1;
      } while (DAT_1000b5d0 <= puVar1);
    }
    FUN_10003ad9((undefined4 *)&DAT_10009018,(undefined4 *)&DAT_10009020);
  }
  FUN_10003ad9((undefined4 *)&DAT_10009024,(undefined4 *)&DAT_10009028);
  if (param_3 == 0) {
    DAT_10009fb8 = 1;
                    /* WARNING: Subroutine does not return */
    ExitProcess(param_1);
  }
  FUN_10003ad0();
  return;
}


