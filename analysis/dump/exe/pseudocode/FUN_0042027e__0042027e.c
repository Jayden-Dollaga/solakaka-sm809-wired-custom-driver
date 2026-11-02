// Program: SM809 mouse Software.exe
// Function: FUN_0042027e
// Entry: 0042027e
// Body: 0042027e - 004202a5
// Signature: undefined FUN_0042027e(_EXCEPTION_POINTERS * param_1)


void __cdecl FUN_0042027e(_EXCEPTION_POINTERS *param_1)

{
  HANDLE hProcess;
  UINT uExitCode;
  
  SetUnhandledExceptionFilter((LPTOP_LEVEL_EXCEPTION_FILTER)0x0);
  UnhandledExceptionFilter(param_1);
  uExitCode = 0xc0000409;
  hProcess = GetCurrentProcess();
  TerminateProcess(hProcess,uExitCode);
  return;
}


