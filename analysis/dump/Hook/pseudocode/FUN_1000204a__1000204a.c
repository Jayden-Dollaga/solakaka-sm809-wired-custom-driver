// Program: Hook.dll
// Function: FUN_1000204a
// Entry: 1000204a
// Body: 1000204a - 100020ec
// Signature: undefined FUN_1000204a(UINT param_1, int param_2, int param_3)


void __cdecl FUN_1000204a(UINT param_1,int param_2,int param_3)

{
  HANDLE hProcess;
  undefined4 *puVar1;
  UINT uExitCode;
  
  FUN_100020ef();
  if (DAT_10007d84 == 1) {
    uExitCode = param_1;
    hProcess = GetCurrentProcess();
    TerminateProcess(hProcess,uExitCode);
  }
  DAT_10007d80 = 1;
  DAT_10007d7c = (undefined1)param_3;
  if (param_2 == 0) {
    if ((DAT_10009410 != (undefined4 *)0x0) &&
       (puVar1 = (undefined4 *)(DAT_1000940c - 4), DAT_10009410 <= puVar1)) {
      do {
        if ((code *)*puVar1 != (code *)0x0) {
          (*(code *)*puVar1)();
        }
        puVar1 = puVar1 + -1;
      } while (DAT_10009410 <= puVar1);
    }
    FUN_10002101((undefined4 *)&DAT_10007018,(undefined4 *)&DAT_10007020);
  }
  FUN_10002101((undefined4 *)&DAT_10007024,(undefined4 *)&DAT_10007028);
  if (param_3 == 0) {
    DAT_10007d84 = 1;
                    /* WARNING: Subroutine does not return */
    ExitProcess(param_1);
  }
  FUN_100020f8();
  return;
}


