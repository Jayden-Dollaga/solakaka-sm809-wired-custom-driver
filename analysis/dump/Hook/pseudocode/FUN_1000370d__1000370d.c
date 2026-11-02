// Program: Hook.dll
// Function: FUN_1000370d
// Entry: 1000370d
// Body: 1000370d - 10003756
// Signature: int FUN_1000370d(int param_1)


int __cdecl FUN_1000370d(int param_1)

{
  int iVar1;
  bool bVar2;
  
  if (param_1 == -2) {
    DAT_10007ef8 = 1;
                    /* WARNING: Could not recover jumptable at 0x10003727. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    iVar1 = GetOEMCP();
    return iVar1;
  }
  if (param_1 == -3) {
    DAT_10007ef8 = 1;
                    /* WARNING: Could not recover jumptable at 0x1000373c. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    iVar1 = GetACP();
    return iVar1;
  }
  bVar2 = param_1 == -4;
  if (bVar2) {
    param_1 = DAT_10007f2c;
  }
  DAT_10007ef8 = (uint)bVar2;
  return param_1;
}


