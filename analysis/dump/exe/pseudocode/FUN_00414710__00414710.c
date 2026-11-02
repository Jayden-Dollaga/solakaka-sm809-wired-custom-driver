// Program: SM809 mouse Software.exe
// Function: FUN_00414710
// Entry: 00414710
// Body: 00414710 - 00414809
// Signature: undefined FUN_00414710(byte * param_1)


void __fastcall FUN_00414710(byte *param_1)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  byte bVar4;
  byte bVar5;
  byte bVar6;
  byte bVar7;
  byte bVar8;
  
  bVar1 = param_1[5];
  bVar2 = param_1[2];
  bVar7 = param_1[4];
  bVar6 = param_1[1];
  bVar8 = param_1[3];
  bVar4 = *param_1;
  bVar5 = param_1[6];
  bVar3 = param_1[7];
  param_1[7] = bVar2;
  *param_1 = bVar1;
  param_1[4] = bVar6;
  param_1[1] = bVar7;
  param_1[2] = bVar3;
  param_1[3] = bVar5;
  param_1[5] = bVar4;
  param_1[6] = bVar8;
  bVar7 = bVar7 ^ DAT_00432ab1;
  param_1[1] = bVar7;
  bVar3 = bVar3 ^ DAT_00432ab2;
  param_1[2] = bVar3;
  bVar5 = bVar5 ^ DAT_00432ab3;
  param_1[3] = bVar5;
  bVar6 = bVar6 ^ DAT_00432ab4;
  param_1[4] = bVar6;
  bVar4 = bVar4 ^ DAT_00432ab5;
  param_1[5] = bVar4;
  bVar8 = bVar8 ^ DAT_00432ab6;
  *param_1 = (bVar1 << 3 | bVar7 >> 5) + 0x25;
  param_1[1] = (bVar7 << 3 | bVar3 >> 5) - 10;
  param_1[2] = (bVar3 << 3 | bVar5 >> 5) - 0x1c;
  param_1[3] = (bVar5 << 3 | bVar6 >> 5) + 0x76;
  param_1[4] = (bVar6 << 3 | bVar4 >> 5) + 0x47;
  param_1[5] = (bVar4 << 3 | bVar8 >> 5) + 0x54;
  param_1[6] = (bVar8 << 3 | bVar2 >> 5) - 0x1a;
  param_1[7] = (bVar2 << 3 | bVar1 >> 5) + 0x76;
  return;
}


