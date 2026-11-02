// Program: SM809 mouse Software.exe
// Function: FUN_00409ff0
// Entry: 00409ff0
// Body: 00409ff0 - 0040a033
// Signature: undefined FUN_00409ff0(void * this, int param_1)


void __thiscall FUN_00409ff0(void *this,int param_1)

{
  int iVar1;
  
  iVar1 = *(int *)(param_1 + 0x108);
  if (iVar1 == *(int *)((int)this + 0x764)) {
                    /* WARNING: Could not recover jumptable at 0x0040a00c. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    DuiLib::CWindowWnd::Close(this,1);
    return;
  }
  if ((iVar1 == *(int *)((int)this + 0x768)) || (iVar1 == *(int *)((int)this + 0x76c))) {
                    /* WARNING: Could not recover jumptable at 0x0040a02a. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    DuiLib::CWindowWnd::Close(this,0);
    return;
  }
  return;
}


