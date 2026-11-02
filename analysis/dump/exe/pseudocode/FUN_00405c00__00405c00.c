// Program: SM809 mouse Software.exe
// Function: FUN_00405c00
// Entry: 00405c00
// Body: 00405c00 - 00405c71
// Signature: undefined4 * FUN_00405c00(int param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

undefined4 * __fastcall FUN_00405c00(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_c;
  undefined4 local_8;
  
  local_8 = DAT_00432008 ^ (int)register0x00000010 - 4U;
  local_c = 0;
  iVar2 = GdipCloneImage(*(undefined4 *)(param_1 + 4),&local_c);
  if (iVar2 != 0) {
    *(int *)(param_1 + 8) = iVar2;
  }
  puVar3 = (undefined4 *)GdipAlloc(0x10);
  if (puVar3 == (undefined4 *)0x0) {
    return (undefined4 *)0x0;
  }
  *puVar3 = 0;
  puVar3[1] = 0;
  puVar3[2] = 0;
  puVar3[3] = 0;
  uVar1 = *(undefined4 *)(param_1 + 8);
  *puVar3 = Gdiplus::Image::vftable;
  puVar3[1] = local_c;
  puVar3[2] = uVar1;
  return puVar3;
}


