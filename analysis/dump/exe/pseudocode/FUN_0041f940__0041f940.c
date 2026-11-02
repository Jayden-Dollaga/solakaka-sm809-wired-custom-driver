// Program: SM809 mouse Software.exe
// Function: FUN_0041f940
// Entry: 0041f940
// Body: 0041f940 - 0041f983
// Signature: undefined FUN_0041f940(void * this, int param_1)


void __thiscall FUN_0041f940(void *this,int param_1)

{
  int iVar1;
  
  iVar1 = *(int *)(param_1 + 0x108);
  if (iVar1 == *(int *)((int)this + 0x77c)) {
                    /* WARNING: Could not recover jumptable at 0x0041f95c. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    DuiLib::CWindowWnd::Close(this,1);
    return;
  }
  if ((iVar1 == *(int *)((int)this + 0x780)) || (iVar1 == *(int *)((int)this + 0x784))) {
                    /* WARNING: Could not recover jumptable at 0x0041f97a. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    DuiLib::CWindowWnd::Close(this,0);
    return;
  }
  return;
}


