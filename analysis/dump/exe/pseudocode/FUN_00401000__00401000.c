// Program: SM809 mouse Software.exe
// Function: FUN_00401000
// Entry: 00401000
// Body: 00401000 - 00401038
// Signature: undefined FUN_00401000(void)


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00401000(void)

{
  _DAT_0043201c = operator_new(0x18);
  *(void **)_DAT_0043201c = _DAT_0043201c;
  *(void **)((int)_DAT_0043201c + 4) = _DAT_0043201c;
  *(void **)((int)_DAT_0043201c + 8) = _DAT_0043201c;
  *(undefined2 *)((int)_DAT_0043201c + 0xc) = 0x101;
  _DAT_00432024 = 0;
  _atexit((_func_4879 *)&LAB_00423c20);
  return;
}


