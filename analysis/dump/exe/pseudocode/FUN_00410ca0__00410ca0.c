// Program: SM809 mouse Software.exe
// Function: FUN_00410ca0
// Entry: 00410ca0
// Body: 00410ca0 - 00410d0d
// Signature: undefined FUN_00410ca0(int param_1)


void __fastcall FUN_00410ca0(int param_1)

{
  *(undefined4 *)(param_1 + 0x2c8) = 0;
  *(undefined4 *)(param_1 + 0x2a8) = 0;
  (**(code **)(**(int **)(param_1 + 0x35c) + 0x2c))(L"start_recording_text");
  DuiLib::CCheckBoxUI::SetCheck(*(CCheckBoxUI **)(param_1 + 0x35c),false);
  (**(code **)(param_1 + 0x328))();
  (**(code **)(param_1 + 0x31c))();
  (**(code **)(param_1 + 800))(0);
  (**(code **)(param_1 + 0x32c))(0);
  *(undefined4 *)(param_1 + 0x2ac) = 0;
  FUN_004116c0(param_1);
  return;
}


