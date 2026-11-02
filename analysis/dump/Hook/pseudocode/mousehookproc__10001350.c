// Program: Hook.dll
// Function: mousehookproc
// Entry: 10001350
// Body: 10001350 - 100014d3
// Signature: LRESULT mousehookproc(int param_1, WPARAM param_2, WPARAM * param_3)


/* __stdcall mousehookproc,12 */

LRESULT mousehookproc(int param_1,WPARAM param_2,WPARAM *param_3)

{
  uint uVar1;
  WPARAM WVar2;
  LRESULT LVar3;
  WPARAM wParam;
  CHAR local_104 [260];
  
                    /* 0x1350  7  _mousehookproc@12 */
  if ((param_1 < 0) || ((param_3[3] & 1) != 0)) {
    LVar3 = CallNextHookEx((HHOOK)0x0,param_1,param_2,(LPARAM)param_3);
    return LVar3;
  }
  if (DAT_10007d20 == 1) {
    if ((((((param_2 == 0x205) || (param_2 == 0x204)) || (param_2 == 0x201)) ||
         ((param_2 == 0x202 || (param_2 == 0x208)))) ||
        ((param_2 == 0x207 || ((param_2 == 0x20a || (param_2 == 0x20b)))))) || (param_2 == 0x20c)) {
      FUN_100014e0(local_104,(byte *)s_ms__x_1000706c,param_2);
      uVar1 = param_3[2];
      FUN_100014e0(local_104,(byte *)s_sendlparam___d_1000705c,uVar1 >> 0x10);
      OutputDebugStringA(local_104);
      PostMessageA(DAT_1000a00c,0x501,param_2,uVar1 >> 0x10);
      return 1;
    }
    if ((param_2 == 0x200) && (DAT_10007d24 == 1)) {
      WVar2 = *param_3;
      if ((int)WVar2 < 1) {
        wParam = 0;
      }
      else {
        wParam = DAT_10007d14;
        if ((int)WVar2 < (int)DAT_10007d14) {
          wParam = WVar2;
        }
      }
      WVar2 = param_3[1];
      if ((int)WVar2 < 1) {
        WVar2 = 0;
      }
      else if ((int)DAT_10007d10 <= (int)WVar2) {
        WVar2 = DAT_10007d10;
      }
      PostMessageA(DAT_1000a00c,0x502,wParam,WVar2);
    }
  }
  LVar3 = CallNextHookEx(DAT_1000a008,param_1,param_2,(LPARAM)param_3);
  return LVar3;
}


