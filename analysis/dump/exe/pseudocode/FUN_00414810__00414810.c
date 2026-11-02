// Program: SM809 mouse Software.exe
// Function: FUN_00414810
// Entry: 00414810
// Body: 00414810 - 00414906
// Signature: undefined FUN_00414810(byte * param_1)


void __fastcall FUN_00414810(byte *param_1)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  byte bVar4;
  byte bVar5;
  byte bVar6;
  byte bVar7;
  byte bVar8;
  
  bVar3 = param_1[1];
  bVar2 = (byte)(bVar3 + 10) >> 3 | (*param_1 - 0x25) * ' ';
  param_1[1] = bVar2;
  bVar1 = param_1[2];
  bVar8 = (byte)(bVar1 + 0x1c) >> 3 | (bVar3 + 10) * ' ';
  bVar3 = param_1[3];
  param_1[2] = bVar8;
  bVar6 = (byte)(bVar3 + 0x8a) >> 3 | (bVar1 + 0x1c) * ' ';
  bVar1 = param_1[4];
  param_1[3] = bVar6;
  bVar4 = (byte)(bVar1 + 0xb9) >> 3 | (bVar3 + 0x8a) * ' ';
  bVar3 = param_1[5];
  param_1[4] = bVar4;
  bVar1 = (byte)(bVar3 + 0xac) >> 3 | (bVar1 + 0xb9) * ' ';
  param_1[5] = bVar1;
  bVar7 = (byte)(param_1[6] + 0x1a) >> 3 | (bVar3 + 0xac) * ' ';
  bVar5 = (byte)(param_1[7] + 0x8a) >> 3 | (param_1[6] + 0x1a) * ' ';
  param_1[6] = bVar7;
  bVar3 = (byte)(*param_1 - 0x25) >> 3 | (param_1[7] + 0x8a) * ' ';
  param_1[7] = bVar5;
  *param_1 = bVar3;
  bVar2 = bVar2 ^ DAT_00432ab1;
  param_1[1] = bVar2;
  bVar8 = bVar8 ^ DAT_00432ab2;
  param_1[2] = bVar8;
  bVar6 = bVar6 ^ DAT_00432ab3;
  param_1[3] = bVar6;
  bVar4 = bVar4 ^ DAT_00432ab4;
  param_1[4] = bVar4;
  bVar1 = bVar1 ^ DAT_00432ab5;
  param_1[5] = bVar1;
  bVar7 = bVar7 ^ DAT_00432ab6;
  param_1[5] = bVar3;
  *param_1 = bVar1;
  param_1[4] = bVar2;
  param_1[1] = bVar4;
  param_1[7] = bVar8;
  param_1[2] = bVar5;
  param_1[6] = bVar6;
  param_1[3] = bVar7;
  return;
}


