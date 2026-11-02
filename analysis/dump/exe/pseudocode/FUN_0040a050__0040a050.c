// Program: SM809 mouse Software.exe
// Function: FUN_0040a050
// Entry: 0040a050
// Body: 0040a050 - 0040a079
// Signature: undefined FUN_0040a050(CNotifyPump * param_1)


void __fastcall FUN_0040a050(CNotifyPump *param_1)

{
  *(undefined ***)param_1 = CGunPage::vftable;
  DuiLib::CStdPtrArray::~CStdPtrArray((CStdPtrArray *)(param_1 + 0x19c));
  DuiLib::CStdPtrArray::~CStdPtrArray((CStdPtrArray *)(param_1 + 400));
                    /* WARNING: Could not recover jumptable at 0x0040a074. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  DuiLib::CNotifyPump::~CNotifyPump(param_1);
  return;
}


