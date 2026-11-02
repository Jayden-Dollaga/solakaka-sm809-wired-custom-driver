// Program: SM809 mouse Software.exe
// Function: FUN_0040edd0
// Entry: 0040edd0
// Body: 0040edd0 - 0040ee0a
// Signature: undefined FUN_0040edd0(CNotifyPump * param_1)


void __fastcall FUN_0040edd0(CNotifyPump *param_1)

{
  *(undefined ***)param_1 = CMacroPage::vftable;
  if (*(HMODULE *)(param_1 + 0x2f0) != (HMODULE)0x0) {
    FreeLibrary(*(HMODULE *)(param_1 + 0x2f0));
  }
  DuiLib::CStdPtrArray::~CStdPtrArray((CStdPtrArray *)(param_1 + 0x304));
  DuiLib::CStdPtrArray::~CStdPtrArray((CStdPtrArray *)(param_1 + 0x2f8));
                    /* WARNING: Could not recover jumptable at 0x0040ee05. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  DuiLib::CNotifyPump::~CNotifyPump(param_1);
  return;
}


