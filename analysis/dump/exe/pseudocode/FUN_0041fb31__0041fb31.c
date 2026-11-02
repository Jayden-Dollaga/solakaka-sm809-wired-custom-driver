// Program: SM809 mouse Software.exe
// Function: FUN_0041fb31
// Entry: 0041fb31
// Body: 0041fb31 - 0041fb61
// Signature: undefined FUN_0041fb31(int param_1)


void __fastcall FUN_0041fb31(int param_1)

{
  code *pcVar1;
  undefined4 *puVar2;
  undefined4 uVar3;
  
  pcVar1 = *(code **)(**(int **)(param_1 + 4) + 8);
  guard_check_icall();
  puVar2 = (undefined4 *)(*pcVar1)();
  if (puVar2 != (undefined4 *)0x0) {
    uVar3 = 1;
    pcVar1 = *(code **)*puVar2;
    guard_check_icall();
    (*pcVar1)(uVar3);
  }
  return;
}


