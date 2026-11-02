// Program: SM809 mouse Software.exe
// Function: ___scrt_get_show_window_mode
// Entry: 004209fc
// Body: 004209fc - 00420a2c
// Signature: WORD ___scrt_get_show_window_mode(void)


/* Library Function - Single Match
    ___scrt_get_show_window_mode
   
   Libraries: Visual Studio 2017 Release, Visual Studio 2019 Release */

WORD ___scrt_get_show_window_mode(void)

{
  _STARTUPINFOW local_48;
  
  memset(&local_48,0,0x44);
  GetStartupInfoW(&local_48);
  if (((byte)local_48.dwFlags & 1) == 0) {
    return 10;
  }
  return local_48.wShowWindow;
}


