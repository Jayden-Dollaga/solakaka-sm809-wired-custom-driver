// Program: SM809 mouse Software.exe
// Function: FUN_00406db0
// Entry: 00406db0
// Body: 00406db0 - 004081dc
// Signature: undefined FUN_00406db0(void * param_1, CDuiString param_2)


/* WARNING: Function: __alloca_probe replaced with injection: alloca_probe */
/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_00406db0(void *param_1,CDuiString param_2)

{
  char cVar1;
  void *pvVar2;
  int iVar3;
  CControlUI *pCVar4;
  uint uVar5;
  char *pcVar6;
  int iVar7;
  char cVar8;
  byte bVar9;
  void *this;
  int iVar10;
  wchar_t *pwVar11;
  wchar_t *pwVar12;
  code *pcVar13;
  int iVar14;
  undefined4 *puVar15;
  bool bVar16;
  char acStack_1fd0 [32];
  char acStack_1fb0 [32];
  CControlUI *local_1f90;
  wchar_t *local_1f8c;
  int local_1f88;
  wchar_t *local_1f84;
  void *local_1f80;
  undefined **local_1f7c [4];
  undefined **local_1f6c;
  undefined **local_1f5c;
  undefined **local_1f58;
  undefined **local_1f54;
  undefined **local_1f50;
  CPaintManagerUI local_1f4c [1856];
  CControlUI *local_180c;
  undefined4 local_17f4;
  undefined4 local_17f0;
  CStdPtrArray local_17ec [12];
  CStdPtrArray local_17e0 [12];
  undefined4 local_17d4;
  uint local_17d0;
  undefined1 local_17cc;
  undefined **local_17c8 [4];
  undefined **local_17b8;
  undefined **local_17a8;
  undefined **local_17a4;
  undefined **local_17a0;
  undefined **local_179c;
  undefined1 local_1050;
  undefined4 local_104c;
  undefined4 local_1048;
  undefined **local_1044 [4];
  undefined **local_1034;
  undefined **local_1024;
  undefined **local_1020;
  undefined **local_101c;
  undefined **local_1018;
  undefined1 local_8a8;
  HMODULE local_8a4;
  undefined4 local_8a0;
  undefined1 local_89c;
  undefined **local_898 [4];
  undefined **local_888;
  undefined **local_878;
  undefined **local_874;
  undefined **local_870;
  undefined **local_86c;
  undefined **local_7d8 [4];
  undefined **local_7c8;
  undefined **local_7b8;
  undefined **local_7b4;
  undefined **local_7b0;
  undefined **local_7ac;
  CPaintManagerUI local_7a8 [1676];
  CDuiString local_11c [132];
  CDuiString local_98 [48];
  CControlUI *local_68;
  undefined4 local_48;
  undefined4 local_44;
  CStdPtrArray local_40 [12];
  CStdPtrArray local_34 [12];
  undefined4 local_28;
  uint local_24;
  undefined4 local_20;
  uint local_1c;
  undefined1 local_18;
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined1 local_8;
  undefined1 auStack_7 [3];
  
  puStack_c = &LAB_00421817;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(auStack_7 + 3);
  ExceptionList = &local_10;
  local_8 = 0;
  auStack_7 = (undefined1  [3])0x0;
  iVar14 = *(int *)((int)param_1 + 0x18) * 0x72c + DAT_00432aa0;
  local_1f84 = (wchar_t *)(iVar14 + 0x150);
  local_1f88 = iVar14;
  local_1f80 = param_1;
  iVar3 = DuiLib::CDuiString::CompareNoCase(&param_2,L"click");
  if (iVar3 == 0) {
    cVar8 = '\x01';
  }
  else {
    iVar3 = DuiLib::CDuiString::CompareNoCase(&param_2,L"menu");
    if (iVar3 == 0) {
      cVar8 = '\x02';
    }
    else {
      iVar3 = DuiLib::CDuiString::CompareNoCase(&param_2,L"scroll");
      if (iVar3 == 0) {
        cVar8 = '\x03';
      }
      else {
        iVar3 = DuiLib::CDuiString::CompareNoCase(&param_2,L"forward");
        if (iVar3 == 0) {
          cVar8 = '\x04';
        }
        else {
          iVar3 = DuiLib::CDuiString::CompareNoCase(&param_2,L"backward");
          if (iVar3 == 0) {
            cVar8 = '\x05';
          }
          else {
            iVar3 = DuiLib::CDuiString::CompareNoCase(&param_2,L"scroll_up");
            if (iVar3 == 0) {
              cVar8 = '\v';
            }
            else {
              iVar3 = DuiLib::CDuiString::CompareNoCase(&param_2,L"scroll_down");
              if (iVar3 == 0) {
                cVar8 = '\f';
              }
              else {
                iVar3 = DuiLib::CDuiString::CompareNoCase(&param_2,L"double_click");
                if (iVar3 == 0) {
                  cVar8 = '\t';
                }
                else {
                  iVar3 = DuiLib::CDuiString::CompareNoCase(&param_2,L"three_click");
                  if (iVar3 == 0) {
                    cVar8 = '\x12';
                  }
                  else {
                    iVar3 = DuiLib::CDuiString::CompareNoCase(&param_2,L"fire_click");
                    if (iVar3 == 0) {
                      cVar8 = '\n';
                    }
                    else {
                      iVar3 = DuiLib::CDuiString::CompareNoCase(&param_2,L"send_gun");
                      if (iVar3 == 0) {
                        cVar8 = '\x19';
                      }
                      else {
                        iVar3 = DuiLib::CDuiString::CompareNoCase(&param_2,L"juji");
                        if (iVar3 == 0) {
                          cVar8 = 'q';
                        }
                        else {
                          iVar3 = DuiLib::CDuiString::CompareNoCase(&param_2,L"mode_switch");
                          if (iVar3 == 0) {
                            cVar8 = '\x1a';
                          }
                          else {
                            iVar3 = DuiLib::CDuiString::CompareNoCase(&param_2,L"light_mode_switch")
                            ;
                            if (iVar3 == 0) {
                              cVar8 = '2';
                            }
                            else {
                              iVar3 = DuiLib::CDuiString::CompareNoCase(&param_2,L"button_off");
                              if (iVar3 == 0) {
                                cVar8 = '\0';
                              }
                              else {
                                iVar3 = DuiLib::CDuiString::CompareNoCase(&param_2,L"shortcut");
                                if (iVar3 == 0) {
                                  cVar8 = '\x15';
                                }
                                else {
                                  iVar3 = DuiLib::CDuiString::CompareNoCase
                                                    (&param_2,L"select_macro");
                                  if (iVar3 == 0) {
                                    cVar8 = '\x16';
                                  }
                                  else {
                                    iVar3 = DuiLib::CDuiString::CompareNoCase
                                                      (&param_2,L"select_gun");
                                    if (iVar3 == 0) {
                                      cVar8 = 'y';
                                    }
                                    else {
                                      iVar3 = DuiLib::CDuiString::CompareNoCase
                                                        (&param_2,L"dpi_cycle");
                                      if (iVar3 == 0) {
                                        cVar8 = '\x06';
                                      }
                                      else {
                                        iVar3 = DuiLib::CDuiString::CompareNoCase
                                                          (&param_2,L"dpi_up");
                                        if (iVar3 == 0) {
                                          cVar8 = '\a';
                                        }
                                        else {
                                          iVar3 = DuiLib::CDuiString::CompareNoCase
                                                            (&param_2,L"dpi_down");
                                          if (iVar3 == 0) {
                                            cVar8 = '\b';
                                          }
                                          else {
                                            iVar3 = DuiLib::CDuiString::CompareNoCase
                                                              (&param_2,L"report_cycle");
                                            if (iVar3 == 0) {
                                              cVar8 = 'p';
                                            }
                                            else {
                                              iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                (&param_2,L"report_up");
                                              if (iVar3 == 0) {
                                                cVar8 = 'h';
                                              }
                                              else {
                                                iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                  (&param_2,L"report_down");
                                                if (iVar3 == 0) {
                                                  cVar8 = 'i';
                                                }
                                                else {
                                                  iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                    (&param_2,L"media_player");
                                                  if (iVar3 == 0) {
                                                    cVar8 = '@';
                                                  }
                                                  else {
                                                    iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                      (&param_2,L"play_pause");
                                                    if (iVar3 == 0) {
                                                      cVar8 = 'A';
                                                    }
                                                    else {
                                                      iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                        (&param_2,L"media_stop");
                                                      if (iVar3 == 0) {
                                                        cVar8 = 'B';
                                                      }
                                                      else {
                                                        iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                          (&param_2,L"pre_track");
                                                        if (iVar3 == 0) {
                                                          cVar8 = 'C';
                                                        }
                                                        else {
                                                          iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                            (&param_2,L"next_track")
                                                          ;
                                                          if (iVar3 == 0) {
                                                            cVar8 = 'D';
                                                          }
                                                          else {
                                                            iVar3 = DuiLib::CDuiString::
                                                                    CompareNoCase(&param_2,
                                                  L"volume_up");
                                                  if (iVar3 == 0) {
                                                    cVar8 = 'E';
                                                  }
                                                  else {
                                                    iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                      (&param_2,L"volume_down");
                                                    if (iVar3 == 0) {
                                                      cVar8 = 'F';
                                                    }
                                                    else {
                                                      iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                        (&param_2,L"mute");
                                                      if (iVar3 == 0) {
                                                        cVar8 = 'G';
                                                      }
                                                      else {
                                                        iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                          (&param_2,L"browser_home")
                                                        ;
                                                        if (iVar3 == 0) {
                                                          cVar8 = 'H';
                                                        }
                                                        else {
                                                          iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                            (&param_2,
                                                  L"browser_favorites");
                                                  if (iVar3 == 0) {
                                                    cVar8 = 'I';
                                                  }
                                                  else {
                                                    iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                      (&param_2,L"browser_forward");
                                                    if (iVar3 == 0) {
                                                      cVar8 = 'J';
                                                    }
                                                    else {
                                                      iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                        (&param_2,
                                                  L"browser_backward");
                                                  if (iVar3 == 0) {
                                                    cVar8 = 'K';
                                                  }
                                                  else {
                                                    iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                      (&param_2,L"browser_stop");
                                                    if (iVar3 == 0) {
                                                      cVar8 = 'L';
                                                    }
                                                    else {
                                                      iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                        (&param_2,L"browser_refresh"
                                                                        );
                                                      if (iVar3 == 0) {
                                                        cVar8 = 'M';
                                                      }
                                                      else {
                                                        iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                          (&param_2,
                                                  L"browser_search");
                                                  if (iVar3 == 0) {
                                                    cVar8 = 'N';
                                                  }
                                                  else {
                                                    iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                      (&param_2,L"email");
                                                    if (iVar3 == 0) {
                                                      cVar8 = 'O';
                                                    }
                                                    else {
                                                      iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                        (&param_2,L"calculator");
                                                      if (iVar3 == 0) {
                                                        cVar8 = 'P';
                                                      }
                                                      else {
                                                        iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                          (&param_2,L"my_computer");
                                                        if (iVar3 == 0) {
                                                          cVar8 = 'Q';
                                                        }
                                                        else {
                                                          iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                            (&param_2,L"cut");
                                                          if (iVar3 == 0) {
                                                            cVar8 = ' ';
                                                          }
                                                          else {
                                                            iVar3 = DuiLib::CDuiString::
                                                                    CompareNoCase(&param_2,L"copy");
                                                            if (iVar3 == 0) {
                                                              cVar8 = '!';
                                                            }
                                                            else {
                                                              iVar3 = DuiLib::CDuiString::
                                                                      CompareNoCase(&param_2,
                                                  L"paste");
                                                  if (iVar3 == 0) {
                                                    cVar8 = '\"';
                                                  }
                                                  else {
                                                    iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                      (&param_2,L"open");
                                                    if (iVar3 == 0) {
                                                      cVar8 = '#';
                                                    }
                                                    else {
                                                      iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                        (&param_2,L"save");
                                                      if (iVar3 == 0) {
                                                        cVar8 = '$';
                                                      }
                                                      else {
                                                        iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                          (&param_2,L"find");
                                                        if (iVar3 == 0) {
                                                          cVar8 = '%';
                                                        }
                                                        else {
                                                          iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                            (&param_2,L"redo");
                                                          if (iVar3 == 0) {
                                                            cVar8 = '&';
                                                          }
                                                          else {
                                                            iVar3 = DuiLib::CDuiString::
                                                                    CompareNoCase(&param_2,
                                                  L"select_all");
                                                  if (iVar3 == 0) {
                                                    cVar8 = '(';
                                                  }
                                                  else {
                                                    iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                      (&param_2,L"new");
                                                    if (iVar3 == 0) {
                                                      cVar8 = '/';
                                                    }
                                                    else {
                                                      iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                        (&param_2,L"print");
                                                      if (iVar3 == 0) {
                                                        cVar8 = ')';
                                                      }
                                                      else {
                                                        iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                          (&param_2,L"swap_windows")
                                                        ;
                                                        if (iVar3 == 0) {
                                                          cVar8 = '+';
                                                        }
                                                        else {
                                                          iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                            (&param_2,
                                                  L"close_windows");
                                                  if (iVar3 == 0) {
                                                    cVar8 = '*';
                                                  }
                                                  else {
                                                    iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                      (&param_2,L"show_desktop");
                                                    if (iVar3 == 0) {
                                                      cVar8 = ',';
                                                    }
                                                    else {
                                                      iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                        (&param_2,L"lock_pc");
                                                      if (iVar3 == 0) {
                                                        cVar8 = '.';
                                                      }
                                                      else {
                                                        iVar3 = DuiLib::CDuiString::CompareNoCase
                                                                          (&param_2,L"run_command");
                                                        cVar8 = (-(iVar3 != 0) & 0xd4U) + 0x2d;
                                                      }
                                                    }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                  }
                                                }
                                              }
                                            }
                                          }
                                        }
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  pvVar2 = local_1f80;
  iVar3 = DAT_00432aa0;
  bVar16 = false;
  if (*(int *)(DAT_00432aa0 + 0x14c) == 0) {
    iVar7 = 0;
    pcVar6 = (char *)(DAT_00432aa0 + 0x219);
    do {
      cVar1 = *pcVar6;
      pcVar6 = pcVar6 + 0x72c;
      acStack_1fd0[iVar7] = cVar1;
      iVar7 = iVar7 + 1;
    } while (iVar7 < 0x1e);
    acStack_1fd0[*(int *)((int)local_1f80 + 0x18)] = cVar8;
    iVar7 = 0;
    do {
      if ((acStack_1fd0[iVar7] == '\x01') || (acStack_1fd0[iVar7] == '\x19')) {
        bVar16 = true;
      }
      if ((acStack_1fd0[iVar7 + 1] == '\x01') || (acStack_1fd0[iVar7 + 1] == '\x19')) {
        bVar16 = true;
      }
      if ((acStack_1fd0[iVar7 + 2] == '\x01') || (acStack_1fd0[iVar7 + 2] == '\x19')) {
        bVar16 = true;
      }
      if ((acStack_1fd0[iVar7 + 3] == '\x01') || (acStack_1fd0[iVar7 + 3] == '\x19')) {
        bVar16 = true;
      }
      if ((acStack_1fd0[iVar7 + 4] == '\x01') || (acStack_1fd0[iVar7 + 4] == '\x19')) {
        bVar16 = true;
      }
      if ((acStack_1fd0[iVar7 + 5] == '\x01') || (acStack_1fd0[iVar7 + 5] == '\x19')) {
        bVar16 = true;
      }
      iVar7 = iVar7 + 6;
    } while (iVar7 < 0x1e);
  }
  else {
    iVar7 = 0x20;
    pcVar6 = (char *)(DAT_00432aa0 + 0xe799);
    do {
      cVar1 = *pcVar6;
      pcVar6 = pcVar6 + 0x72c;
      acStack_1fd0[iVar7] = cVar1;
      iVar7 = iVar7 + 1;
    } while (iVar7 < 0x40);
    acStack_1fd0[*(int *)((int)local_1f80 + 0x18)] = cVar8;
    iVar7 = 0x20;
    do {
      if ((acStack_1fd0[iVar7] == '\x01') || (acStack_1fd0[iVar7] == '\x19')) {
        bVar16 = true;
      }
      if ((acStack_1fd0[iVar7 + 1] == '\x01') || (acStack_1fd0[iVar7 + 1] == '\x19')) {
        bVar16 = true;
      }
      if ((acStack_1fd0[iVar7 + 2] == '\x01') || (acStack_1fd0[iVar7 + 2] == '\x19')) {
        bVar16 = true;
      }
      if ((acStack_1fd0[iVar7 + 3] == '\x01') || (acStack_1fd0[iVar7 + 3] == '\x19')) {
        bVar16 = true;
      }
      iVar7 = iVar7 + 4;
    } while (iVar7 < 0x40);
  }
  this = local_1f80;
  if (!bVar16) {
    memset(local_898,0,0x884);
    FUN_0041c1c0((WindowImplBase *)local_898);
    local_8 = 1;
    DuiLib::CDuiString::operator=(local_11c,L"warning_title_text");
    DuiLib::CDuiString::operator=(local_98,L"one_left_click_text");
    DuiLib::CWindowWnd::Create
              ((CWindowWnd *)local_898,*(HWND__ **)((int)local_1f80 + 0x14),L"MsgWnd",0x90000000,
               0x80,0,0,800,800,(HMENU__ *)0x0);
    DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_898);
    DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_898);
    pcVar13 = ~CDuiString_exref;
    local_898[0] = CMsgWnd::vftable;
    local_888 = CMsgWnd::vftable;
    local_878 = CMsgWnd::vftable;
    local_874 = CMsgWnd::vftable;
    local_870 = CMsgWnd::vftable;
    local_86c = CMsgWnd::vftable;
    DuiLib::CDuiString::~CDuiString(local_98);
    DuiLib::CDuiString::~CDuiString(local_11c);
    DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_898);
    goto LAB_00408126;
  }
  if (cVar8 == '\x15') {
    pCVar4 = DuiLib::CPaintManagerUI::FindControl
                       (*(CPaintManagerUI **)((int)pvVar2 + 0x10),L"disable_window_ver");
    (**(code **)(*(int *)pCVar4 + 0xf8))(1);
    if (*(char *)(iVar14 + 0x219) == '\x15') {
      bVar9 = *(byte *)(iVar14 + 0x22c);
    }
    else {
      *(undefined2 *)(iVar14 + 0x22c) = 0;
      bVar9 = 0;
    }
    memset(local_1044,0,0x7ac);
    DuiLib::WindowImplBase::WindowImplBase((WindowImplBase *)local_1044);
    this = local_1f80;
    local_1044[0] = CShortcutWnd::vftable;
    local_1034 = CShortcutWnd::vftable;
    local_1024 = CShortcutWnd::vftable;
    local_1020 = CShortcutWnd::vftable;
    local_101c = CShortcutWnd::vftable;
    local_1018 = CShortcutWnd::vftable;
    local_8a8 = 0;
    local_8a4 = (HMODULE)0x0;
    local_8 = 2;
    local_89c = *(undefined1 *)(iVar14 + 0x22d);
    local_8a0 = CONCAT13(bVar9 >> 3,CONCAT12(bVar9 >> 2,CONCAT11(bVar9 >> 1,bVar9))) & 0x1010101;
    DuiLib::CWindowWnd::Create
              ((CWindowWnd *)local_1044,*(HWND__ **)((int)local_1f80 + 0x14),L"ShortcutWnd",
               0x90000000,0x80,0,0,800,800,(HMENU__ *)0x0);
    DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_1044);
    uVar5 = DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_1044);
    if (uVar5 == 1) {
      *(undefined1 *)(iVar14 + 0x22d) = local_89c;
      bVar9 = (char)local_8a0 == '\x01';
      if (local_8a0._1_1_ == '\x01') {
        bVar9 = bVar9 | 2;
      }
      if (local_8a0._2_1_ == '\x01') {
        bVar9 = bVar9 | 4;
      }
      if (local_8a0._3_1_ == '\x01') {
        bVar9 = bVar9 | 8;
      }
      *(byte *)(iVar14 + 0x22c) = bVar9;
      (**(code **)(*(int *)pCVar4 + 0xf8))(0);
      local_8 = 0;
      local_1044[0] = CShortcutWnd::vftable;
      local_1034 = CShortcutWnd::vftable;
      local_1024 = CShortcutWnd::vftable;
      local_1020 = CShortcutWnd::vftable;
      local_101c = CShortcutWnd::vftable;
      local_1018 = CShortcutWnd::vftable;
      if (local_8a4 != (HMODULE)0x0) {
        FreeLibrary(local_8a4);
        local_8a4 = (HMODULE)0x0;
      }
      DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_1044);
      *(undefined1 *)(iVar14 + 0x219) = 0x15;
LAB_00408116:
      FUN_004081e0(this,*(int *)((int)this + 0x18));
    }
    else {
      (**(code **)(*(int *)pCVar4 + 0xf8))(0);
      local_1044[0] = CShortcutWnd::vftable;
      local_1034 = CShortcutWnd::vftable;
      local_1024 = CShortcutWnd::vftable;
      local_1020 = CShortcutWnd::vftable;
      local_101c = CShortcutWnd::vftable;
      local_1018 = CShortcutWnd::vftable;
      if (local_8a4 != (HMODULE)0x0) {
        FreeLibrary(local_8a4);
        local_8a4 = (HMODULE)0x0;
      }
      DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_1044);
    }
  }
  else if (cVar8 == '\n') {
    pCVar4 = DuiLib::CPaintManagerUI::FindControl
                       (*(CPaintManagerUI **)((int)local_1f80 + 0x10),L"disable_window_ver");
    (**(code **)(*(int *)pCVar4 + 0xf8))(1);
    if (*(char *)(iVar14 + 0x219) != '\n') {
      *(undefined4 *)(iVar14 + 0x82c) = 0;
      *(undefined4 *)(iVar14 + 0x830) = 2;
    }
    memset(local_17c8,0,0x784);
    DuiLib::WindowImplBase::WindowImplBase((WindowImplBase *)local_17c8);
    local_17c8[0] = CFireClickWnd::vftable;
    local_17b8 = CFireClickWnd::vftable;
    local_17a8 = CFireClickWnd::vftable;
    local_17a4 = CFireClickWnd::vftable;
    local_17a0 = CFireClickWnd::vftable;
    local_179c = CFireClickWnd::vftable;
    local_1050 = 0;
    local_8 = 3;
    local_104c = *(undefined4 *)(iVar14 + 0x82c);
    local_1048 = *(undefined4 *)(iVar14 + 0x830);
    DuiLib::CWindowWnd::Create
              ((CWindowWnd *)local_17c8,*(HWND__ **)((int)this + 0x14),L"ShortcutWnd",0x90000000,
               0x80,0,0,800,800,(HMENU__ *)0x0);
    DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_17c8);
    uVar5 = DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_17c8);
    if (uVar5 == 1) {
      *(undefined4 *)(iVar14 + 0x82c) = local_104c;
      *(undefined4 *)(iVar14 + 0x830) = local_1048;
      (**(code **)(*(int *)pCVar4 + 0xf8))();
      local_8 = 0;
      local_17c8[0] = CFireClickWnd::vftable;
      local_17b8 = CFireClickWnd::vftable;
      local_17a8 = CFireClickWnd::vftable;
      local_17a4 = CFireClickWnd::vftable;
      local_17a0 = CFireClickWnd::vftable;
      local_179c = CFireClickWnd::vftable;
      DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_17c8);
      *(undefined1 *)(iVar14 + 0x219) = 10;
      goto LAB_00408116;
    }
    (**(code **)(*(int *)pCVar4 + 0xf8))(0);
    local_17c8[0] = CFireClickWnd::vftable;
    local_17b8 = CFireClickWnd::vftable;
    local_17a8 = CFireClickWnd::vftable;
    local_17a4 = CFireClickWnd::vftable;
    local_17a0 = CFireClickWnd::vftable;
    local_179c = CFireClickWnd::vftable;
    DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_17c8);
  }
  else if (cVar8 == '\x16') {
    if (*(char *)(iVar14 + 0x219) != '\x16') {
      iVar7 = 0;
      *(undefined4 *)(iVar14 + 0x220) = 0xffffffff;
      *(undefined4 *)(iVar14 + 0x224) = 0;
      *(undefined4 *)(iVar14 + 0x5a8) = 0xff;
      iVar10 = 0x10;
      pcVar6 = (char *)(iVar3 + 0x945);
      do {
        iVar3 = iVar7 + 1;
        if (pcVar6[-0x72c] != '\x16') {
          iVar3 = iVar7;
        }
        iVar7 = iVar3 + 1;
        if (*pcVar6 != '\x16') {
          iVar7 = iVar3;
        }
        iVar3 = iVar7 + 1;
        if (pcVar6[0x72c] != '\x16') {
          iVar3 = iVar7;
        }
        iVar7 = iVar3 + 1;
        if (pcVar6[0xe58] != '\x16') {
          iVar7 = iVar3;
        }
        iVar10 = iVar10 + -1;
        pcVar6 = pcVar6 + 0x1cb0;
      } while (iVar10 != 0);
      if (9 < iVar7) goto LAB_00408120;
    }
    pCVar4 = DuiLib::CPaintManagerUI::FindControl
                       (*(CPaintManagerUI **)((int)local_1f80 + 0x10),L"disable_window_ver");
    local_1f90 = pCVar4;
    (**(code **)(*(int *)pCVar4 + 0xf8))(1);
    memset(local_7d8,0,0x7c4);
    DuiLib::WindowImplBase::WindowImplBase((WindowImplBase *)local_7d8);
    local_8 = 4;
    local_7d8[0] = CSelectMacroWnd::vftable;
    local_7c8 = CSelectMacroWnd::vftable;
    local_7b8 = CSelectMacroWnd::vftable;
    local_7b4 = CSelectMacroWnd::vftable;
    local_7b0 = CSelectMacroWnd::vftable;
    local_7ac = CSelectMacroWnd::vftable;
    DuiLib::CStdPtrArray::CStdPtrArray(local_40,0);
    local_8 = 5;
    DuiLib::CStdPtrArray::CStdPtrArray(local_34,0);
    local_8 = 6;
    local_18 = 0;
    local_48 = 0;
    DuiLib::CStdPtrArray::Empty(local_34);
    DuiLib::CStdPtrArray::Empty(local_40);
    local_28 = 0xffffffff;
    local_20 = 0;
    local_44 = 0xff;
    local_8 = 7;
    bVar16 = *(char *)(iVar14 + 0x219) == '9';
    local_24 = *(uint *)(iVar14 + 0x220);
    local_48 = *(undefined4 *)(iVar14 + 0x224);
    if (bVar16) {
      local_44 = *(undefined4 *)(iVar14 + 0x5a8);
    }
    local_1c = (uint)bVar16;
    DuiLib::CWindowWnd::Create
              ((CWindowWnd *)local_7d8,*(HWND__ **)((int)local_1f80 + 0x14),L"SelectMacroWnd",
               0x90000000,0x80,0,0,800,800,(HMENU__ *)0x0);
    DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_7d8);
    DuiLib::CPaintManagerUI::SetTimer(local_7a8,local_68,1000,100);
    uVar5 = DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_7d8);
    if (((uVar5 == 1) && (DAT_0046c380 != DAT_0046c384)) && (-1 < (int)local_24)) {
      if ((uint)(DAT_0046c384 - DAT_0046c380 >> 2) <= local_24) {
                    /* WARNING: Subroutine does not return */
        FUN_004050f0();
      }
      pwVar12 = *(wchar_t **)(DAT_0046c380 + local_24 * 4);
      local_1f8c = pwVar12;
      if ((pwVar12 != (wchar_t *)0x0) && (pwVar12[0x66] != L'\0')) {
        *(uint *)(iVar14 + 0x220) = local_24;
        *(undefined4 *)(iVar14 + 0x224) = local_48;
        *(wchar_t *)(iVar14 + 0x232) = pwVar12[0x66];
        memset((wchar_t *)(iVar14 + 0x1b4),0,100);
        wcscpy_s(local_1f84,0x32,pwVar12);
        pwVar12 = local_1f8c;
        wcscpy_s((wchar_t *)(iVar14 + 0x1b4),0x32,local_1f8c + 0x32);
        iVar14 = local_1f88;
        pwVar11 = pwVar12 + 0x6c;
        puVar15 = (undefined4 *)(local_1f88 + 0x5ac);
        for (iVar3 = 0xa0; iVar3 != 0; iVar3 = iVar3 + -1) {
          *puVar15 = *(undefined4 *)pwVar11;
          pwVar11 = pwVar11 + 2;
          puVar15 = puVar15 + 1;
        }
        *(uint *)(local_1f88 + 0x234) = (uint)(ushort)pwVar12[100];
        if (local_1c == 1) {
          cVar8 = '9';
          *(undefined4 *)(local_1f88 + 0x5a8) = local_44;
        }
        else {
          cVar8 = '\x16';
          *(undefined4 *)(local_1f88 + 0x5a8) = 0xff;
        }
        (**(code **)(*(int *)local_1f90 + 0xf8))(0);
        local_8 = 0;
        local_7d8[0] = CSelectMacroWnd::vftable;
        local_7c8 = CSelectMacroWnd::vftable;
        local_7b8 = CSelectMacroWnd::vftable;
        local_7b4 = CSelectMacroWnd::vftable;
        local_7b0 = CSelectMacroWnd::vftable;
        local_7ac = CSelectMacroWnd::vftable;
        DuiLib::CStdPtrArray::~CStdPtrArray(local_34);
        DuiLib::CStdPtrArray::~CStdPtrArray(local_40);
        DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_7d8);
        goto LAB_00407d01;
      }
    }
    (**(code **)(*(int *)pCVar4 + 0xf8))(0);
    local_7d8[0] = CSelectMacroWnd::vftable;
    local_7c8 = CSelectMacroWnd::vftable;
    local_7b8 = CSelectMacroWnd::vftable;
    local_7b4 = CSelectMacroWnd::vftable;
    local_7b0 = CSelectMacroWnd::vftable;
    local_7ac = CSelectMacroWnd::vftable;
    DuiLib::CStdPtrArray::~CStdPtrArray(local_34);
    DuiLib::CStdPtrArray::~CStdPtrArray(local_40);
    DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_7d8);
  }
  else {
    if (cVar8 != 'y') {
LAB_00407d01:
      this = local_1f80;
      *(char *)(iVar14 + 0x219) = cVar8;
      if (cVar8 == '\x1a') {
        iVar14 = *(int *)((int)local_1f80 + 0x18) * 0x72c;
        if (*(int *)((int)local_1f80 + 0x18) < 0x20) {
          *(undefined1 *)(iVar14 + 0xe799 + DAT_00432aa0) = 0x1a;
          FUN_004081e0(local_1f80,*(int *)((int)local_1f80 + 0x18) + 0x20);
        }
        else {
          *(undefined1 *)(iVar14 + -0xe367 + DAT_00432aa0) = 0x1a;
          FUN_004081e0(local_1f80,*(int *)((int)local_1f80 + 0x18) + -0x20);
        }
        goto LAB_00408116;
      }
LAB_00408110:
      this = local_1f80;
      goto LAB_00408116;
    }
    if ((*(char *)(iVar14 + 0x219) != 'y') && (*(char *)(iVar14 + 0x219) != '9')) {
      iVar7 = 0;
      *(undefined4 *)(iVar14 + 0x21c) = 0xffffffff;
      pcVar6 = (char *)(iVar3 + 0x945);
      *(undefined4 *)(iVar14 + 0x224) = 0;
      *(undefined4 *)(iVar14 + 0x5a8) = 0xff;
      iVar3 = 0x10;
      do {
        if ((pcVar6[-0x72c] == 'y') || (pcVar6[-0x72c] == '9')) {
          iVar7 = iVar7 + 1;
        }
        if ((*pcVar6 == 'y') || (*pcVar6 == '9')) {
          iVar7 = iVar7 + 1;
        }
        if ((pcVar6[0x72c] == 'y') || (pcVar6[0x72c] == '9')) {
          iVar7 = iVar7 + 1;
        }
        if ((pcVar6[0xe58] == 'y') || (pcVar6[0xe58] == '9')) {
          iVar7 = iVar7 + 1;
        }
        pcVar6 = pcVar6 + 0x1cb0;
        iVar3 = iVar3 + -1;
      } while (iVar3 != 0);
      if (2 < iVar7) goto LAB_00408120;
    }
    pCVar4 = DuiLib::CPaintManagerUI::FindControl
                       (*(CPaintManagerUI **)((int)local_1f80 + 0x10),L"disable_window_ver");
    (**(code **)(*(int *)pCVar4 + 0xf8))(1);
    memset(local_1f7c,0,0x7b4);
    DuiLib::WindowImplBase::WindowImplBase((WindowImplBase *)local_1f7c);
    local_8 = 8;
    local_1f7c[0] = CSelectGunWnd::vftable;
    local_1f6c = CSelectGunWnd::vftable;
    local_1f5c = CSelectGunWnd::vftable;
    local_1f58 = CSelectGunWnd::vftable;
    local_1f54 = CSelectGunWnd::vftable;
    local_1f50 = CSelectGunWnd::vftable;
    DuiLib::CStdPtrArray::CStdPtrArray(local_17ec,0);
    local_8 = 9;
    DuiLib::CStdPtrArray::CStdPtrArray(local_17e0,0);
    local_8 = 10;
    local_17cc = 0;
    local_17f4 = 0;
    local_17f0 = 0xff;
    DuiLib::CStdPtrArray::Empty(local_17e0);
    DuiLib::CStdPtrArray::Empty(local_17ec);
    local_17d4 = 0xffffffff;
    local_8 = 0xb;
    local_17d0 = *(uint *)(iVar14 + 0x21c);
    local_17f4 = *(undefined4 *)(iVar14 + 0x224);
    local_17f0 = *(undefined4 *)(iVar14 + 0x5a8);
    DuiLib::CWindowWnd::Create
              ((CWindowWnd *)local_1f7c,*(HWND__ **)((int)local_1f80 + 0x14),L"SelectMacroWnd",
               0x90000000,0x80,0,0,800,800,(HMENU__ *)0x0);
    DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_1f7c);
    DuiLib::CPaintManagerUI::SetTimer(local_1f4c,local_180c,1000,100);
    uVar5 = DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_1f7c);
    if (((uVar5 == 1) && (DAT_0046c398 != DAT_0046c39c)) && (-1 < (int)local_17d0)) {
      if ((uint)(DAT_0046c39c - DAT_0046c398 >> 2) <= local_17d0) {
                    /* WARNING: Subroutine does not return */
        FUN_004050f0();
      }
      local_1f84 = *(wchar_t **)(DAT_0046c398 + local_17d0 * 4);
      if (local_1f84 != (wchar_t *)0x0) {
        *(undefined4 *)(iVar14 + 0x224) = local_17f4;
        *(uint *)(iVar14 + 0x21c) = local_17d0;
        *(undefined4 *)(iVar14 + 0x5a8) = local_17f0;
        *(ushort *)(iVar14 + 0x232) = (ushort)(byte)local_1f84[100];
        memset((wchar_t *)(iVar14 + 0x1b4),0,100);
        wcscpy_s((wchar_t *)(iVar14 + 0x1b4),0x32,local_1f84 + 0x32);
        wcscpy_s((wchar_t *)(iVar14 + 0x150),0x32,local_1f84);
        iVar3 = local_1f88;
        pwVar12 = local_1f84 + 0x6c;
        puVar15 = (undefined4 *)(iVar14 + 0x440);
        for (iVar7 = 0x5a; iVar7 != 0; iVar7 = iVar7 + -1) {
          *puVar15 = *(undefined4 *)pwVar12;
          pwVar12 = pwVar12 + 2;
          puVar15 = puVar15 + 1;
        }
        *(uint *)(local_1f88 + 0x234) = (uint)(byte)local_1f84[0x65];
        (**(code **)(*(int *)pCVar4 + 0xf8))(0);
        local_8 = 0;
        local_1f7c[0] = CSelectGunWnd::vftable;
        local_1f6c = CSelectGunWnd::vftable;
        local_1f5c = CSelectGunWnd::vftable;
        local_1f58 = CSelectGunWnd::vftable;
        local_1f54 = CSelectGunWnd::vftable;
        local_1f50 = CSelectGunWnd::vftable;
        DuiLib::CStdPtrArray::~CStdPtrArray(local_17e0);
        DuiLib::CStdPtrArray::~CStdPtrArray(local_17ec);
        DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_1f7c);
        *(undefined1 *)(iVar3 + 0x219) = 0x79;
        goto LAB_00408110;
      }
    }
    (**(code **)(*(int *)pCVar4 + 0xf8))(0);
    local_1f7c[0] = CSelectGunWnd::vftable;
    local_1f6c = CSelectGunWnd::vftable;
    local_1f5c = CSelectGunWnd::vftable;
    local_1f58 = CSelectGunWnd::vftable;
    local_1f54 = CSelectGunWnd::vftable;
    local_1f50 = CSelectGunWnd::vftable;
    DuiLib::CStdPtrArray::~CStdPtrArray(local_17e0);
    DuiLib::CStdPtrArray::~CStdPtrArray(local_17ec);
    DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_1f7c);
  }
LAB_00408120:
  pcVar13 = ~CDuiString_exref;
LAB_00408126:
  (*pcVar13)();
  ExceptionList = local_10;
  return;
}


