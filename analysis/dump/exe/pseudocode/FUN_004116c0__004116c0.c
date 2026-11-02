// Program: SM809 mouse Software.exe
// Function: FUN_004116c0
// Entry: 004116c0
// Body: 004116c0 - 0041173e
// Signature: undefined FUN_004116c0(int param_1)


void __fastcall FUN_004116c0(int param_1)

{
  int iVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  undefined4 in_stack_ffffffe8;
  undefined4 in_stack_ffffffec;
  
  iVar1 = *(int *)(param_1 + 0x1c);
  if ((iVar1 != 0) && (*(int *)(iVar1 + 0xd0) == 0)) {
    puVar3 = (undefined4 *)(param_1 + 0x24);
    puVar4 = (undefined4 *)(iVar1 + 0xd8);
    for (iVar2 = 0xa0; iVar2 != 0; iVar2 = iVar2 + -1) {
      *puVar4 = *puVar3;
      puVar3 = puVar3 + 1;
      puVar4 = puVar4 + 1;
    }
    *(undefined2 *)(*(int *)(param_1 + 0x1c) + 0xcc) = *(undefined2 *)(param_1 + 0x2a4);
    *(undefined2 *)(*(int *)(param_1 + 0x1c) + 200) = *(undefined2 *)(param_1 + 0x2f4);
    FUN_00402ef0();
    iVar1 = FUN_004040e0(*(uint *)(param_1 + 0x314),DAT_00432aa8,in_stack_ffffffe8,in_stack_ffffffec
                         ,0);
    if (iVar1 != 0) {
      SendMessageW(*(HWND *)(param_1 + 0x14),0x467,0,0);
    }
  }
  return;
}


