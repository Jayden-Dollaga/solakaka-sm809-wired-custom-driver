// Program: MSDriver.dll
// Function: FUN_10001470
// Entry: 10001470
// Body: 10001470 - 100014a2
// Signature: undefined FUN_10001470(int param_1, uint param_2)


void __cdecl FUN_10001470(int param_1,uint param_2)

{
  PostMessageA(DAT_10009ec8,DAT_10009ec4,(uint)(param_1 != 0),param_2 & 0xffff);
  return;
}


