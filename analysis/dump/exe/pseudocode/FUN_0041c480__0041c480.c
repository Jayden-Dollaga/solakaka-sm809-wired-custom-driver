// Program: SM809 mouse Software.exe
// Function: FUN_0041c480
// Entry: 0041c480
// Body: 0041c480 - 0041c48b
// Signature: undefined FUN_0041c480(CNotifyPump * param_1)


void __fastcall FUN_0041c480(CNotifyPump *param_1)

{
  *(undefined ***)param_1 = CPerformancePage::vftable;
                    /* WARNING: Could not recover jumptable at 0x0041c486. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  DuiLib::CNotifyPump::~CNotifyPump(param_1);
  return;
}


