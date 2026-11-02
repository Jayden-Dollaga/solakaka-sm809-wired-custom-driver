// Program: SM809 mouse Software.exe
// Function: FUN_0041d110
// Entry: 0041d110
// Body: 0041d110 - 0041d618
// Signature: undefined FUN_0041d110(int param_1)


void __fastcall FUN_0041d110(int param_1)

{
  undefined4 *puVar1;
  int iVar2;
  
  if (DAT_00432ad8 == 0xcfd) {
    puVar1 = (undefined4 *)(param_1 + 0x68);
    iVar2 = 8;
    do {
      (**(code **)(*(int *)puVar1[0x10] + 0x2c))(&DAT_004299ec);
      (**(code **)(*(int *)puVar1[0x18] + 0x2c))(L"10000");
      DuiLib::CProgressUI::SetMinValue((CProgressUI *)*puVar1,2);
      DuiLib::CProgressUI::SetMaxValue((CProgressUI *)*puVar1,100);
      puVar1 = puVar1 + 1;
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
    return;
  }
  if (DAT_00432ad8 == 0xc8c) {
    puVar1 = (undefined4 *)(param_1 + 0x68);
    iVar2 = 8;
    do {
      (**(code **)(*(int *)puVar1[0x10] + 0x2c))(&DAT_00429a00);
      (**(code **)(*(int *)puVar1[0x18] + 0x2c))(L"7560");
      DuiLib::CProgressUI::SetMinValue((CProgressUI *)*puVar1,1);
      DuiLib::CProgressUI::SetMaxValue((CProgressUI *)*puVar1,0xbd);
      puVar1 = puVar1 + 1;
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
    return;
  }
  if (DAT_00432ad8 == 0xbea) {
    puVar1 = (undefined4 *)(param_1 + 0x68);
    iVar2 = 8;
    do {
      (**(code **)(*(int *)puVar1[0x10] + 0x2c))(&DAT_00424f68);
      (**(code **)(*(int *)puVar1[0x18] + 0x2c))(L"4000");
      DuiLib::CProgressUI::SetMinValue((CProgressUI *)*puVar1,1);
      DuiLib::CProgressUI::SetMaxValue((CProgressUI *)*puVar1,0xc);
      puVar1 = puVar1 + 1;
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
    return;
  }
  if (DAT_00432ad8 == 0x13ba) {
    puVar1 = (undefined4 *)(param_1 + 0x68);
    iVar2 = 8;
    do {
      (**(code **)(*(int *)puVar1[0x10] + 0x2c))(&DAT_00429a14);
      (**(code **)(*(int *)puVar1[0x18] + 0x2c))(L"2750");
      DuiLib::CProgressUI::SetMinValue((CProgressUI *)*puVar1,1);
      DuiLib::CProgressUI::SetMaxValue((CProgressUI *)*puVar1,0x11);
      puVar1 = puVar1 + 1;
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
    return;
  }
  if (DAT_00432ad8 == 0xcff) {
    puVar1 = (undefined4 *)(param_1 + 0x68);
    iVar2 = 8;
    do {
      (**(code **)(*(int *)puVar1[0x10] + 0x2c))(&DAT_004299ec);
      (**(code **)(*(int *)puVar1[0x18] + 0x2c))(L"12000");
      DuiLib::CProgressUI::SetMinValue((CProgressUI *)*puVar1,2);
      DuiLib::CProgressUI::SetMaxValue((CProgressUI *)*puVar1,0x78);
      puVar1 = puVar1 + 1;
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
    return;
  }
  if (DAT_00432ad8 == 0xd07) {
    puVar1 = (undefined4 *)(param_1 + 0x68);
    iVar2 = 8;
    do {
      (**(code **)(*(int *)puVar1[0x10] + 0x2c))(&DAT_00429a34);
      (**(code **)(*(int *)puVar1[0x18] + 0x2c))(L"19000");
      DuiLib::CProgressUI::SetMinValue((CProgressUI *)*puVar1,1);
      DuiLib::CProgressUI::SetMaxValue((CProgressUI *)*puVar1,0xa0);
      puVar1 = puVar1 + 1;
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
    return;
  }
  if (DAT_00432ad8 == 0x24) {
    puVar1 = (undefined4 *)(param_1 + 0x68);
    iVar2 = 8;
    do {
      (**(code **)(*(int *)puVar1[0x10] + 0x2c))(&DAT_00429a34);
      (**(code **)(*(int *)puVar1[0x18] + 0x2c))(L"8000");
      DuiLib::CProgressUI::SetMinValue((CProgressUI *)*puVar1,1);
      DuiLib::CProgressUI::SetMaxValue((CProgressUI *)*puVar1,0x50);
      puVar1 = puVar1 + 1;
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
    return;
  }
  if (DAT_00432ad8 == 0x25) {
    puVar1 = (undefined4 *)(param_1 + 0x68);
    iVar2 = 8;
    do {
      (**(code **)(*(int *)puVar1[0x10] + 0x2c))(&DAT_00429a34);
      (**(code **)(*(int *)puVar1[0x18] + 0x2c))(L"12000");
      DuiLib::CProgressUI::SetMinValue((CProgressUI *)*puVar1,1);
      DuiLib::CProgressUI::SetMaxValue((CProgressUI *)*puVar1,0x78);
      puVar1 = puVar1 + 1;
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
    return;
  }
  if (DAT_00432ad8 == 0x26) {
    puVar1 = (undefined4 *)(param_1 + 0x68);
    iVar2 = 8;
    do {
      (**(code **)(*(int *)puVar1[0x10] + 0x2c))(&DAT_00429a34);
      (**(code **)(*(int *)puVar1[0x18] + 0x2c))(L"16000");
      DuiLib::CProgressUI::SetMinValue((CProgressUI *)*puVar1,1);
      DuiLib::CProgressUI::SetMaxValue((CProgressUI *)*puVar1,0xa0);
      puVar1 = puVar1 + 1;
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
    return;
  }
  if (DAT_00432ad8 == 0x3c) {
    puVar1 = (undefined4 *)(param_1 + 0x68);
    iVar2 = 8;
    do {
      (**(code **)(*(int *)puVar1[0x10] + 0x2c))(&DAT_00429a34);
      (**(code **)(*(int *)puVar1[0x18] + 0x2c))(L"24000");
      DuiLib::CProgressUI::SetMinValue((CProgressUI *)*puVar1,1);
      DuiLib::CProgressUI::SetMaxValue((CProgressUI *)*puVar1,0xf0);
      puVar1 = puVar1 + 1;
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
    return;
  }
  if (DAT_00432ad8 == 0x1900) {
    puVar1 = (undefined4 *)(param_1 + 0x68);
    iVar2 = 8;
    do {
      (**(code **)(*(int *)puVar1[0x10] + 0x2c))(&DAT_004299ec);
      (**(code **)(*(int *)puVar1[0x18] + 0x2c))(L"12400");
      DuiLib::CProgressUI::SetMinValue((CProgressUI *)*puVar1,4);
      DuiLib::CProgressUI::SetMaxValue((CProgressUI *)*puVar1,0xf8);
      puVar1 = puVar1 + 1;
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
    return;
  }
  if (DAT_00432ad8 == 0xc20) {
    puVar1 = (undefined4 *)(param_1 + 0x68);
    iVar2 = 8;
    do {
      (**(code **)(*(int *)puVar1[0x10] + 0x2c))(&DAT_00429a6c);
      (**(code **)(*(int *)puVar1[0x18] + 0x2c))(L"8480");
      DuiLib::CProgressUI::SetMinValue((CProgressUI *)*puVar1,0x10);
      DuiLib::CProgressUI::SetMaxValue((CProgressUI *)*puVar1,0xd4);
      puVar1 = puVar1 + 1;
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
    return;
  }
  if (DAT_00432ad8 == 0xd02) {
    puVar1 = (undefined4 *)(param_1 + 0x68);
    iVar2 = 8;
    do {
      (**(code **)(*(int *)puVar1[0x10] + 0x2c))(&DAT_00429a80);
      (**(code **)(*(int *)puVar1[0x18] + 0x2c))(L"7200");
      DuiLib::CProgressUI::SetMinValue((CProgressUI *)*puVar1,1);
      DuiLib::CProgressUI::SetMaxValue((CProgressUI *)*puVar1,0x90);
      puVar1 = puVar1 + 1;
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
    return;
  }
  if (DAT_00432ad8 == 0xd05) {
    puVar1 = (undefined4 *)(param_1 + 0x68);
    iVar2 = 8;
    do {
      (**(code **)(*(int *)puVar1[0x10] + 0x2c))(&DAT_004299ec);
      (**(code **)(*(int *)puVar1[0x18] + 0x2c))(L"16000");
      DuiLib::CProgressUI::SetMinValue((CProgressUI *)*puVar1,2);
      DuiLib::CProgressUI::SetMaxValue((CProgressUI *)*puVar1,0xa0);
      puVar1 = puVar1 + 1;
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
    return;
  }
  if (DAT_00432ad8 == 0xd2a) {
    puVar1 = (undefined4 *)(param_1 + 0x68);
    iVar2 = 8;
    do {
      (**(code **)(*(int *)puVar1[0x10] + 0x2c))(&DAT_00429a80);
      (**(code **)(*(int *)puVar1[0x18] + 0x2c))(L"19000");
      DuiLib::CProgressUI::SetMinValue((CProgressUI *)*puVar1,1);
      DuiLib::CProgressUI::SetMaxValue((CProgressUI *)*puVar1,0x122);
      puVar1 = puVar1 + 1;
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
    return;
  }
  if (DAT_00432ad8 == 0xcef) {
    puVar1 = (undefined4 *)(param_1 + 0x68);
    iVar2 = 8;
    do {
      (**(code **)(*(int *)puVar1[0x10] + 0x2c))(&DAT_00429a34);
      (**(code **)(*(int *)puVar1[0x18] + 0x2c))(L"24000");
      DuiLib::CProgressUI::SetMinValue((CProgressUI *)*puVar1,1);
      DuiLib::CProgressUI::SetMaxValue((CProgressUI *)*puVar1,0xf0);
      puVar1 = puVar1 + 1;
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
  }
  return;
}


