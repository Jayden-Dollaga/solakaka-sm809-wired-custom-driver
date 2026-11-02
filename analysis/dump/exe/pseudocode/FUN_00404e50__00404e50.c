// Program: SM809 mouse Software.exe
// Function: FUN_00404e50
// Entry: 00404e50
// Body: 00404e50 - 00404e5f
// Signature: undefined FUN_00404e50(int param_1)


void __fastcall FUN_00404e50(int param_1)

{
  if (*(FILE **)(param_1 + 0x4c) != (FILE *)0x0) {
    _lock_file(*(FILE **)(param_1 + 0x4c));
  }
  return;
}


