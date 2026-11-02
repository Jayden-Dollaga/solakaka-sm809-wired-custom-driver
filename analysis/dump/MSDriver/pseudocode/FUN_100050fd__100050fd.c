// Program: MSDriver.dll
// Function: FUN_100050fd
// Entry: 100050fd
// Body: 100050fd - 10005146
// Signature: int FUN_100050fd(int param_1)


int __cdecl FUN_100050fd(int param_1)

{
  int iVar1;
  bool bVar2;
  
  if (param_1 == -2) {
    DAT_1000a0cc = 1;
                    /* WARNING: Could not recover jumptable at 0x10005117. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    iVar1 = GetOEMCP();
    return iVar1;
  }
  if (param_1 == -3) {
    DAT_1000a0cc = 1;
                    /* WARNING: Could not recover jumptable at 0x1000512c. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    iVar1 = GetACP();
    return iVar1;
  }
  bVar2 = param_1 == -4;
  if (bVar2) {
    param_1 = DAT_1000a100;
  }
  DAT_1000a0cc = (uint)bVar2;
  return param_1;
}


