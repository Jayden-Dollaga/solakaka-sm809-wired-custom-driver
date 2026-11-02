// Program: SM809 mouse Software.exe
// Function: FUN_00402370
// Entry: 00402370
// Body: 00402370 - 00402844
// Signature: CDuiString * FUN_00402370(CDuiString * param_1, undefined4 param_2)


CDuiString * __fastcall FUN_00402370(CDuiString *param_1,undefined4 param_2)

{
  wchar_t *pwVar1;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  puStack_c = &LAB_00420fcf;
  local_10 = ExceptionList;
  ExceptionList = &local_10;
  local_8 = 0;
  DuiLib::CDuiString::CDuiString(param_1);
  local_8 = 0;
  switch(param_2) {
  case 4:
    pwVar1 = L"key_A";
    break;
  case 5:
    pwVar1 = L"key_B";
    break;
  case 6:
    pwVar1 = L"key_C";
    break;
  case 7:
    pwVar1 = L"key_D";
    break;
  case 8:
    pwVar1 = L"key_E";
    break;
  case 9:
    pwVar1 = L"key_F";
    break;
  case 10:
    pwVar1 = L"key_G";
    break;
  case 0xb:
    pwVar1 = L"key_H";
    break;
  case 0xc:
    pwVar1 = L"key_I";
    break;
  case 0xd:
    pwVar1 = L"key_J";
    break;
  case 0xe:
    pwVar1 = L"key_K";
    break;
  case 0xf:
    pwVar1 = L"key_L";
    break;
  case 0x10:
    pwVar1 = L"key_M";
    break;
  case 0x11:
    pwVar1 = L"key_N";
    break;
  case 0x12:
    pwVar1 = L"key_O";
    break;
  case 0x13:
    pwVar1 = L"key_P";
    break;
  case 0x14:
    pwVar1 = L"key_Q";
    break;
  case 0x15:
    pwVar1 = L"key_R";
    break;
  case 0x16:
    pwVar1 = L"key_S";
    break;
  case 0x17:
    pwVar1 = L"key_T";
    break;
  case 0x18:
    pwVar1 = L"key_U";
    break;
  case 0x19:
    pwVar1 = L"key_V";
    break;
  case 0x1a:
    pwVar1 = L"key_W";
    break;
  case 0x1b:
    pwVar1 = L"key_X";
    break;
  case 0x1c:
    pwVar1 = L"key_Y";
    break;
  case 0x1d:
    pwVar1 = L"key_Z";
    break;
  case 0x1e:
    pwVar1 = L"key_1";
    break;
  case 0x1f:
    pwVar1 = L"key_2";
    break;
  case 0x20:
    pwVar1 = L"key_3";
    break;
  case 0x21:
    pwVar1 = L"key_4";
    break;
  case 0x22:
    pwVar1 = L"key_5";
    break;
  case 0x23:
    pwVar1 = L"key_6";
    break;
  case 0x24:
    pwVar1 = L"key_7";
    break;
  case 0x25:
    pwVar1 = L"key_8";
    break;
  case 0x26:
    pwVar1 = L"key_9";
    break;
  case 0x27:
    pwVar1 = L"key_0";
    break;
  case 0x28:
    pwVar1 = L"key_Enter";
    break;
  case 0x29:
    pwVar1 = L"key_Esc";
    break;
  case 0x2a:
    pwVar1 = L"key_BackSpace";
    break;
  case 0x2b:
    pwVar1 = L"key_Tab";
    break;
  case 0x2c:
    pwVar1 = L"key_Space";
    break;
  case 0x2d:
    pwVar1 = L"key_-";
    break;
  case 0x2e:
    pwVar1 = L"key_=";
    break;
  case 0x2f:
    pwVar1 = L"key_[";
    break;
  case 0x30:
    pwVar1 = L"key_]";
    break;
  case 0x31:
  case 100:
    pwVar1 = L"key_Xiexian";
    break;
  case 0x32:
    pwVar1 = L"￥";
    break;
  case 0x33:
    pwVar1 = L"key_;";
    break;
  case 0x34:
    pwVar1 = L"key_\'";
    break;
  case 0x35:
    pwVar1 = L"key_`";
    break;
  case 0x36:
    pwVar1 = L"key_,";
    break;
  case 0x37:
    pwVar1 = L"key_.";
    break;
  case 0x38:
    pwVar1 = L"key_/";
    break;
  case 0x39:
    pwVar1 = L"key_Caplk";
    break;
  case 0x3a:
    pwVar1 = L"key_F1";
    break;
  case 0x3b:
    pwVar1 = L"key_F2";
    break;
  case 0x3c:
    pwVar1 = L"key_F3";
    break;
  case 0x3d:
    pwVar1 = L"key_F4";
    break;
  case 0x3e:
    pwVar1 = L"key_F5";
    break;
  case 0x3f:
    pwVar1 = L"key_F6";
    break;
  case 0x40:
    pwVar1 = L"key_F7";
    break;
  case 0x41:
    pwVar1 = L"key_F8";
    break;
  case 0x42:
    pwVar1 = L"key_F9";
    break;
  case 0x43:
    pwVar1 = L"key_F10";
    break;
  case 0x44:
    pwVar1 = L"key_F11";
    break;
  case 0x45:
    pwVar1 = L"key_F12";
    break;
  case 0x46:
    pwVar1 = L"key_Print Scr";
    break;
  case 0x47:
    pwVar1 = L"key_Scroll Lock";
    break;
  case 0x48:
    pwVar1 = L"key_Pause";
    break;
  case 0x49:
    pwVar1 = L"key_Insert";
    break;
  case 0x4a:
    pwVar1 = L"key_Home";
    break;
  case 0x4b:
    pwVar1 = L"key_Page Up";
    break;
  case 0x4c:
    pwVar1 = L"key_Delete";
    break;
  case 0x4d:
    pwVar1 = L"key_End";
    break;
  case 0x4e:
    pwVar1 = L"key_Page Down";
    break;
  case 0x4f:
    pwVar1 = L"key_Right";
    break;
  case 0x50:
    pwVar1 = L"key_Left";
    break;
  case 0x51:
    pwVar1 = L"key_Down";
    break;
  case 0x52:
    pwVar1 = L"key_Up";
    break;
  case 0x53:
    pwVar1 = L"key_Num Lock";
    break;
  case 0x54:
    pwVar1 = L"key_Num_/";
    break;
  case 0x55:
    pwVar1 = L"key_Num_*";
    break;
  case 0x56:
    pwVar1 = L"key_Num_-";
    break;
  case 0x57:
    pwVar1 = L"key_Num_+";
    break;
  case 0x58:
    pwVar1 = L"key_Num_Enter";
    break;
  case 0x59:
    pwVar1 = L"key_Num_1";
    break;
  case 0x5a:
    pwVar1 = L"key_Num_2";
    break;
  case 0x5b:
    pwVar1 = L"key_Num_3";
    break;
  case 0x5c:
    pwVar1 = L"key_Num_4";
    break;
  case 0x5d:
    pwVar1 = L"key_Num_5";
    break;
  case 0x5e:
    pwVar1 = L"key_Num_6";
    break;
  case 0x5f:
    pwVar1 = L"key_Num_7";
    break;
  case 0x60:
    pwVar1 = L"key_Num_8";
    break;
  case 0x61:
    pwVar1 = L"key_Num_9";
    break;
  case 0x62:
    pwVar1 = L"key_Num_0";
    break;
  case 99:
    pwVar1 = L"key_Num_.";
    break;
  case 0x65:
    pwVar1 = L"key_App";
    break;
  default:
    pwVar1 = L"";
    break;
  case 0x82:
    pwVar1 = L"Sleep";
    break;
  case 0x88:
    pwVar1 = L"Kana/Roma";
    break;
  case 0xdd:
    pwVar1 = L"`";
    break;
  case 0xe0:
    pwVar1 = L"key_LCtrl";
    break;
  case 0xe1:
    pwVar1 = L"key_LShift";
    break;
  case 0xe2:
    pwVar1 = L"key_LAlt";
    break;
  case 0xe3:
    pwVar1 = L"key_LWin";
    break;
  case 0xe4:
    pwVar1 = L"key_RCtrl";
    break;
  case 0xe5:
    pwVar1 = L"key_RShift";
    break;
  case 0xe6:
    pwVar1 = L"key_RAlt";
    break;
  case 0xe7:
    pwVar1 = L"key_RWin";
    break;
  case 0xf0:
    pwVar1 = L"L_Button";
    break;
  case 0xf1:
    pwVar1 = L"R_Button";
    break;
  case 0xf2:
    pwVar1 = L"M_Button";
    break;
  case 0xf3:
    pwVar1 = L"Backward_Button";
    break;
  case 0xf4:
    pwVar1 = L"Forward_Button";
    break;
  case 0xf8:
    pwVar1 = L"Scroll_Up";
    break;
  case 0xf9:
    pwVar1 = L"Scroll_Down";
  }
  DuiLib::CDuiString::operator=(param_1,pwVar1);
  ExceptionList = local_10;
  return param_1;
}


