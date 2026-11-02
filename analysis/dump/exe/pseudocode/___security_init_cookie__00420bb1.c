// Program: SM809 mouse Software.exe
// Function: ___security_init_cookie
// Entry: 00420bb1
// Body: 00420bb1 - 00420bfb
// Signature: void ___security_init_cookie(void)


/* Library Function - Single Match
    ___security_init_cookie
   
   Libraries: Visual Studio 2017 Release, Visual Studio 2019 Release */

void __cdecl ___security_init_cookie(void)

{
  if ((DAT_00432008 == 0xbb40e64e) || ((DAT_00432008 & 0xffff0000) == 0)) {
    DAT_00432008 = ___get_entropy();
    if (DAT_00432008 == 0xbb40e64e) {
      DAT_00432008 = 0xbb40e64f;
    }
    else if ((DAT_00432008 & 0xffff0000) == 0) {
      DAT_00432008 = DAT_00432008 | (DAT_00432008 | 0x4711) << 0x10;
    }
  }
  DAT_00432004 = ~DAT_00432008;
  return;
}


