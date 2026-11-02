// Program: SM809 mouse Software.exe
// Function: FUN_00404e40
// Entry: 00404e40
// Body: 00404e40 - 00404e4f
// Signature: undefined FUN_00404e40(int param_1)


void __fastcall FUN_00404e40(int param_1)

{
  if (*(FILE **)(param_1 + 0x4c) != (FILE *)0x0) {
    _unlock_file(*(FILE **)(param_1 + 0x4c));
  }
  return;
}


