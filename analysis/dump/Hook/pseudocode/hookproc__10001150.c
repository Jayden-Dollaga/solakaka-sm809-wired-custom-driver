// Program: Hook.dll
// Function: hookproc
// Entry: 10001150
// Body: 10001150 - 1000134d
// Signature: LRESULT hookproc(int param_1, WPARAM param_2, WPARAM * param_3)


/* __stdcall hookproc,12 */

LRESULT hookproc(int param_1,WPARAM param_2,WPARAM *param_3)

{
  WPARAM WVar1;
  HWND hWnd;
  LRESULT LVar2;
  DWORD local_10c;
  DWORD local_108;
  undefined1 local_104 [260];
  
                    /* 0x1150  4  _hookproc@12 */
  if ((-1 < param_1) && (DAT_10007d1c == 1)) {
    FUN_100014e0(local_104,(byte *)s_vkCode____x___scanCode____x_flag_10007030,*param_3);
    if (((byte)param_3[2] & 1) != 1) {
      WVar1 = param_3[1];
      if ((WVar1 == 0x47) && (*param_3 == 0x24)) {
        *param_3 = 0x67;
      }
      else if ((WVar1 == 0x48) && (*param_3 == 0x26)) {
        *param_3 = 0x68;
      }
      else if ((WVar1 == 0x49) && (*param_3 == 0x21)) {
        *param_3 = 0x69;
      }
      else if ((WVar1 == 0x4b) && (*param_3 == 0x25)) {
        *param_3 = 100;
      }
      else if ((WVar1 == 0x4c) && (*param_3 == 0xc)) {
        *param_3 = 0x65;
      }
      else if ((WVar1 == 0x4d) && (*param_3 == 0x27)) {
        *param_3 = 0x66;
      }
      else if ((WVar1 == 0x4f) && (*param_3 == 0x23)) {
        *param_3 = 0x61;
      }
      else if ((WVar1 == 0x50) && (*param_3 == 0x28)) {
        *param_3 = 0x62;
      }
      else if ((WVar1 == 0x51) && (*param_3 == 0x22)) {
        *param_3 = 99;
      }
      else if ((WVar1 == 0x52) && (*param_3 == 0x2d)) {
        *param_3 = 0x60;
      }
      else if ((WVar1 == 0x53) && (*param_3 == 0x2e)) {
        *param_3 = 0x6e;
      }
      else if ((WVar1 == 0x79) && (*param_3 == 0xff)) {
        *param_3 = 0xef;
      }
      else if ((WVar1 == 0x70) && (*param_3 == 0xff)) {
        *param_3 = 0xcf;
      }
      else if ((WVar1 == 0x3a) && (*param_3 == 0xf0)) {
        *param_3 = 0xbf;
      }
    }
    if (param_3[1] < 0x100) {
      PostMessageA(DAT_1000a004,0x500,*param_3,param_3[2] & 0x80);
    }
    if (DAT_1000a004 != (HWND)0x0) {
      GetWindowThreadProcessId(DAT_1000a004,&local_108);
      hWnd = GetForegroundWindow();
      GetWindowThreadProcessId(hWnd,&local_10c);
      if (local_108 == local_10c) {
        return 1;
      }
    }
  }
  LVar2 = CallNextHookEx(DAT_1000a000,param_1,param_2,(LPARAM)param_3);
  return LVar2;
}


