// Program: SM809 mouse Software.exe
// Function: FUN_0040dea0
// Entry: 0040dea0
// Body: 0040dea0 - 0040deab
// Signature: undefined FUN_0040dea0(CNotifyPump * param_1)


void __fastcall FUN_0040dea0(CNotifyPump *param_1)

{
  *(undefined ***)param_1 = CLightPage::vftable;
                    /* WARNING: Could not recover jumptable at 0x0040dea6. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  DuiLib::CNotifyPump::~CNotifyPump(param_1);
  return;
}


