// Program: SM809 mouse Software.exe
// Function: __filter_x86_sse2_floating_point_exception_default
// Entry: 00420d85
// Body: 00420d85 - 00420dfc
// Signature: int __filter_x86_sse2_floating_point_exception_default(int param_1)


/* Library Function - Single Match
    __filter_x86_sse2_floating_point_exception_default
   
   Library: Visual Studio 2019 Release */

int __cdecl __filter_x86_sse2_floating_point_exception_default(int param_1)

{
  uint uVar1;
  
  if ((DAT_00432a60 < 1) || ((param_1 != -0x3ffffd4c && (param_1 != -0x3ffffd4b)))) {
    return param_1;
  }
  uVar1 = MXCSR ^ 0x3f;
  if ((uVar1 & 0x81) != 0) {
    if ((uVar1 & 0x204) == 0) {
      return -0x3fffff72;
    }
    if ((uVar1 & 0x102) != 0) {
      if ((uVar1 & 0x408) == 0) {
        return -0x3fffff6f;
      }
      if ((uVar1 & 0x810) == 0) {
        return -0x3fffff6d;
      }
      if ((uVar1 & 0x1020) == 0) {
        return -0x3fffff71;
      }
      return param_1;
    }
  }
  return -0x3fffff70;
}


