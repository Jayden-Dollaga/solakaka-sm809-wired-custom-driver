// Program: SM809 mouse Software.exe
// Function: FUN_00415000
// Entry: 00415000
// Body: 00415000 - 004158a1
// Signature: undefined4 FUN_00415000(void * this, int param_1, wchar_t * param_2, uint param_3, undefined4 * param_4)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

undefined4 __thiscall
FUN_00415000(void *this,int param_1,wchar_t *param_2,uint param_3,undefined4 *param_4)

{
  CMenuWnd *this_00;
  int iVar1;
  int iVar2;
  BOOL BVar3;
  undefined4 uVar4;
  CDuiString *pCVar5;
  WindowImplBase *this_01;
  CDuiString in_stack_fffffcb8;
  CDuiString aCStack_345 [93];
  CDuiString local_2b4 [132];
  CMenuWnd *local_230;
  CDuiString local_22c [132];
  CDuiString local_1a8 [132];
  CDuiString local_124 [132];
  CDuiString local_a0 [132];
  tagPOINT local_1c;
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00422e25;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_a0 + 0x9c);
  ExceptionList = &local_10;
  local_1c.y = (LONG)param_4;
  if (param_1 == 2) {
    PostQuitMessage(0);
  }
  else {
    if (param_1 == 0x403) {
      if (param_2 != (wchar_t *)0x0) {
        DuiLib::CDuiString::CDuiString(local_a0,param_2,-1);
        local_8 = 0;
        DuiLib::CDuiString::CDuiString(local_1a8,param_2 + 0x100,-1);
        local_8._0_1_ = 1;
        DuiLib::CDuiString::CDuiString(local_22c,param_2 + 0x500,-1);
        local_8 = CONCAT31(local_8._1_3_,2);
        DuiLib::CPaintManagerUI::DeletePtr((CPaintManagerUI *)((int)this + 0x30),param_2);
        iVar2 = DuiLib::CDuiString::CompareNoCase(local_a0,L"configuration");
        if (iVar2 == 0) {
          if ((DAT_00432aa4 == 1) && (*(int *)((int)this + 0x16d0) == 1)) {
            BVar3 = IsWindowVisible(*(HWND *)((int)this + 4));
            if (BVar3 == 0) {
              ShowWindow(*(HWND *)((int)this + 4),5);
            }
            BVar3 = IsIconic(*(HWND *)((int)this + 4));
            if (BVar3 != 0) {
              DuiLib::CWindowWnd::SendMessageW(this,0x112,0xf120,0);
            }
            SetForegroundWindow(*(HWND *)((int)this + 4));
          }
          else {
            FUN_0041b6f0((int)this);
          }
        }
        else {
          iVar2 = DuiLib::CDuiString::CompareNoCase(local_a0,L"exit");
          if (iVar2 == 0) {
            DestroyWindow(*(HWND *)((int)this + 4));
          }
          else {
            iVar2 = DuiLib::CDuiString::CompareNoCase(local_a0,L"import_profile");
            if (iVar2 == 0) {
              FUN_004183f0((int)this);
            }
            else {
              iVar2 = DuiLib::CDuiString::CompareNoCase(local_a0,L"export_profile");
              if (iVar2 == 0) {
                FUN_004187c0((int)this);
              }
              else {
                iVar2 = DuiLib::CDuiString::CompareNoCase(local_a0,L"rename_macro_dir");
                if (iVar2 == 0) {
                  FUN_00413970((int)this + 0xb40);
                }
                else {
                  iVar2 = DuiLib::CDuiString::CompareNoCase(local_a0,L"import_macro_dir");
                  if (iVar2 == 0) {
                    FUN_00413c70((int)this + 0xb40);
                  }
                  else {
                    iVar2 = DuiLib::CDuiString::CompareNoCase(local_a0,L"export_macro_dir");
                    if (iVar2 == 0) {
                      FUN_004140e0((int)this + 0xb40);
                    }
                    else {
                      iVar2 = DuiLib::CDuiString::CompareNoCase(local_a0,L"export_pw_macro_dir");
                      if (iVar2 == 0) {
                        FUN_004143e0((int)this + 0xb40);
                      }
                      else {
                        iVar2 = DuiLib::CDuiString::CompareNoCase(local_a0,L"rename_macro");
                        if (iVar2 == 0) {
                          FUN_00411bc0((int)this + 0xb40);
                        }
                        else {
                          iVar2 = DuiLib::CDuiString::CompareNoCase(local_a0,L"import_macro");
                          if (iVar2 == 0) {
                            FUN_00412520((wchar_t *)((int)this + 0xb40));
                          }
                          else {
                            iVar2 = DuiLib::CDuiString::CompareNoCase(local_a0,L"export_macro");
                            if (iVar2 == 0) {
                              FUN_00412cc0((int)this + 0xb40);
                            }
                            else {
                              iVar2 = DuiLib::CDuiString::CompareNoCase(local_a0,L"export_pw_macro")
                              ;
                              if (iVar2 == 0) {
                                FUN_00412f40((int)this + 0xb40);
                              }
                              else {
                                iVar2 = DuiLib::CDuiString::CompareNoCase
                                                  (local_a0,L"rename_gun_dir");
                                if (iVar2 == 0) {
                                  FUN_0040d0f0((int)this + 0xef8);
                                }
                                else {
                                  iVar2 = DuiLib::CDuiString::CompareNoCase
                                                    (local_a0,L"import_gun_dir");
                                  if (iVar2 == 0) {
                                    FUN_0040d3f0((int)this + 0xef8);
                                  }
                                  else {
                                    iVar2 = DuiLib::CDuiString::CompareNoCase
                                                      (local_a0,L"export_gun_dir");
                                    if (iVar2 == 0) {
                                      FUN_0040d860((int)this + 0xef8);
                                    }
                                    else {
                                      iVar2 = DuiLib::CDuiString::CompareNoCase
                                                        (local_a0,L"export_pw_gun_dir");
                                      if (iVar2 == 0) {
                                        FUN_0040db60((int)this + 0xef8);
                                      }
                                      else {
                                        iVar2 = DuiLib::CDuiString::CompareNoCase
                                                          (local_a0,L"rename_gun");
                                        if (iVar2 == 0) {
                                          FUN_0040ba50((int)this + 0xef8);
                                        }
                                        else {
                                          iVar2 = DuiLib::CDuiString::CompareNoCase
                                                            (local_a0,L"import_gun");
                                          if (iVar2 == 0) {
                                            FUN_0040bcf0((wchar_t *)((int)this + 0xef8));
                                          }
                                          else {
                                            iVar2 = DuiLib::CDuiString::CompareNoCase
                                                              (local_a0,L"export_gun");
                                            if (iVar2 == 0) {
                                              FUN_0040c490((int)this + 0xef8);
                                            }
                                            else {
                                              iVar2 = DuiLib::CDuiString::CompareNoCase
                                                                (local_a0,L"export_pw_gun");
                                              if (iVar2 == 0) {
                                                FUN_0040c710((int)this + 0xef8);
                                              }
                                              else {
                                                DuiLib::CDuiString::CDuiString
                                                          (aCStack_345 + -3,local_a0);
                                                FUN_00406db0((void *)((int)this + 0x7a0),
                                                             in_stack_fffffcb8);
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
        DuiLib::CDuiString::~CDuiString(local_22c);
        DuiLib::CDuiString::~CDuiString(local_1a8);
        DuiLib::CDuiString::~CDuiString(local_a0);
        param_4 = (undefined4 *)local_1c.y;
      }
LAB_004153c7:
      *param_4 = 0;
      ExceptionList = local_10;
      return 0;
    }
    if ((param_1 == 0x500) || (param_1 == 0x501)) {
      FUN_00410d10((void *)((int)this + 0xb40),(UINT)param_2,param_3);
    }
    else if (param_1 == 0x467) {
      FUN_00408bc0((void *)((int)this + 0x7a0),*(int *)(DAT_00432aa0 + 0x14c));
      iVar2 = 0;
      do {
        FUN_004081e0((void *)((int)this + 0x7a0),iVar2);
        iVar2 = iVar2 + 1;
      } while (iVar2 < 0x40);
      param_4 = (undefined4 *)local_1c.y;
    }
    else if (param_1 == 0x52d) {
      FUN_004194a0(this,(int)param_2 << 0x10 ^ param_3 & 0xffff);
    }
    else if (param_1 == 0x52e) {
      if (param_2 == (wchar_t *)0x0) {
        FUN_004194a0(this,0x7f000002);
      }
      else {
        FUN_004194a0(this,(param_2 == (wchar_t *)0x1) + 0x7f000000);
      }
    }
    else {
      if (param_1 != 0x40d) {
        if (param_1 == 0x401) {
          if (param_3 == 0x202) {
            if ((DAT_00432aa4 != 1) || (*(int *)((int)this + 0x16d0) != 1)) {
              FUN_0041b6f0((int)this);
              *param_4 = 0;
              ExceptionList = local_10;
              return 0;
            }
            BVar3 = IsWindowVisible(*(HWND *)((int)this + 4));
            if (BVar3 == 0) {
              ShowWindow(*(HWND *)((int)this + 4),5);
            }
            BVar3 = IsIconic(*(HWND *)((int)this + 4));
            if (BVar3 != 0) {
              DuiLib::CWindowWnd::SendMessageW(this,0x112,0xf120,0);
            }
            SetForegroundWindow(*(HWND *)((int)this + 4));
            *param_4 = 0;
            ExceptionList = local_10;
            return 0;
          }
          if (param_3 == 0x205) {
            this_00 = *(CMenuWnd **)((int)this + 0x1720);
            if (this_00 != (CMenuWnd *)0x0) {
              DuiLib::CMenuWnd::~CMenuWnd(this_00);
              FUN_0041feb7(this_00);
              *(undefined4 *)((int)this + 0x1720) = 0;
            }
            local_230 = operator_new(0x770);
            local_8 = 3;
            uVar4 = DuiLib::CMenuWnd::CMenuWnd(local_230);
            local_8 = 0xffffffff;
            *(undefined4 *)((int)this + 0x1720) = uVar4;
            DuiLib::CDuiPoint::CDuiPoint((CDuiPoint *)&local_1c);
            GetCursorPos(&local_1c);
            local_1c.y = local_1c.y + -0x32;
            DuiLib::CMenuWnd::Init(*(CMenuWnd **)((int)this + 0x1720));
            DuiLib::CMenuWnd::ResizeMenu(*(CMenuWnd **)((int)this + 0x1720));
            *param_4 = 0;
            ExceptionList = local_10;
            return 0;
          }
        }
        else if (param_1 == 0x113) {
          if (param_2 == (wchar_t *)0x34) {
            KillTimer(*(HWND *)((int)this + 4),0x34);
            if (*(CWindowWnd **)((int)this + 0x1af4) != (CWindowWnd *)0x0) {
              DuiLib::CWindowWnd::Close(*(CWindowWnd **)((int)this + 0x1af4),0);
              *(undefined4 *)((int)this + 0x1af4) = 0;
              *param_4 = 0;
              ExceptionList = local_10;
              return 0;
            }
          }
        }
        else if (param_1 == 0x469) {
          DuiLib::CDuiString::CDuiString(local_124);
          local_8 = 4;
          DuiLib::CDuiString::operator=(local_124,L"DPI :");
          pCVar5 = FUN_00403d70(local_1a8,param_3);
          local_8._0_1_ = 5;
          DuiLib::CDuiString::operator+=(local_124,pCVar5);
          local_8._0_1_ = 4;
          DuiLib::CDuiString::~CDuiString(local_1a8);
          if (*(int *)((int)this + 0x1af4) == 0) {
            KillTimer(*(HWND *)((int)this + 4),0x34);
            SetTimer(*(HWND *)((int)this + 4),0x34,2000,(TIMERPROC)0x0);
            this_01 = operator_new(0x7f0);
            local_8._0_1_ = 7;
            local_230 = (CMenuWnd *)this_01;
            memset(this_01,0,0x7f0);
            DuiLib::WindowImplBase::WindowImplBase(this_01);
            local_8._0_1_ = 8;
            *(undefined ***)this_01 = CDPIMsg::vftable;
            *(undefined ***)(this_01 + 0x10) = CDPIMsg::vftable;
            *(undefined ***)(this_01 + 0x20) = CDPIMsg::vftable;
            *(undefined ***)(this_01 + 0x24) = CDPIMsg::vftable;
            *(undefined ***)(this_01 + 0x28) = CDPIMsg::vftable;
            *(undefined ***)(this_01 + 0x2c) = CDPIMsg::vftable;
            DuiLib::CDuiString::CDuiString((CDuiString *)(this_01 + 0x76c));
            local_8._0_1_ = 9;
            this_01[0x764] = (WindowImplBase)0x1;
            DuiLib::CDuiString::operator=((CDuiString *)(this_01 + 0x76c),L"");
            local_8 = CONCAT31(local_8._1_3_,4);
            *(WindowImplBase **)((int)this + 0x1af4) = this_01;
            DuiLib::CDuiString::operator=((CDuiString *)(this_01 + 0x76c),local_124);
            DuiLib::CWindowWnd::Create
                      (*(CWindowWnd **)((int)this + 0x1af4),*(HWND__ **)((int)this + 4),
                       (wchar_t *)0x0,0x90000000,0x88,0,0,800,800,(HMENU__ *)0x0);
            *(undefined4 *)local_1c.y = 1;
            DuiLib::CDuiString::~CDuiString(local_124);
            ExceptionList = local_10;
            return 0;
          }
          KillTimer(*(HWND *)((int)this + 4),0x34);
          SetTimer(*(HWND *)((int)this + 4),0x34,2000,(TIMERPROC)0x0);
          DuiLib::CDuiString::CDuiString(local_2b4,local_124);
          iVar2 = *(int *)((int)this + 0x1af4);
          local_8 = CONCAT31(local_8._1_3_,6);
          DuiLib::CDuiString::operator=((CDuiString *)(iVar2 + 0x76c),local_2b4);
          if (*(int **)(iVar2 + 0x768) != (int *)0x0) {
            iVar1 = **(int **)(iVar2 + 0x768);
            DuiLib::CDuiString::operator_wchar_t_const_((CDuiString *)(iVar2 + 0x76c));
            (**(code **)(iVar1 + 0x2c))();
          }
          DuiLib::CDuiString::~CDuiString(local_2b4);
          *(undefined4 *)local_1c.y = 1;
          DuiLib::CDuiString::~CDuiString(local_124);
          ExceptionList = local_10;
          return 0;
        }
        goto LAB_004153c7;
      }
      if ((DAT_00432aa4 == 1) && (*(int *)((int)this + 0x16d0) == 1)) {
        BVar3 = IsWindowVisible(*(HWND *)((int)this + 4));
        if (BVar3 == 0) {
          ShowWindow(*(HWND *)((int)this + 4),5);
        }
        BVar3 = IsIconic(*(HWND *)((int)this + 4));
        if (BVar3 != 0) {
          DuiLib::CWindowWnd::SendMessageW(this,0x112,0xf120,0);
        }
        SetForegroundWindow(*(HWND *)((int)this + 4));
      }
      else {
        FUN_0041b6f0((int)this);
      }
    }
  }
  *param_4 = 1;
  ExceptionList = local_10;
  return 0;
}


