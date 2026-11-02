// Program: SM809 mouse Software.exe
// Function: FUN_00409490
// Entry: 00409490
// Body: 00409490 - 0040993b
// Signature: undefined FUN_00409490(void * this, CDuiString * param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __thiscall FUN_00409490(void *this,CDuiString *param_1)

{
  bool bVar1;
  CDuiString *pCVar2;
  wchar_t *pwVar3;
  int iVar4;
  CDuiString in_stack_fffff5c4;
  CDuiString aCStack_a39 [125];
  CDuiString in_stack_fffff648;
  CDuiString aCStack_9b5 [93];
  undefined **local_91c [4];
  undefined **local_90c;
  undefined **local_8fc;
  undefined **local_8f8;
  undefined **local_8f4;
  undefined **local_8f0;
  CDuiString local_1a0 [132];
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00421aea;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  bVar1 = DuiLib::CDuiString::operator==(param_1,L"click");
  if (bVar1) {
    iVar4 = *(int *)(param_1 + 0x108);
    if (iVar4 == *(int *)((int)this + 0x960)) {
      DuiLib::CDuiString::CDuiString(local_98);
      local_8 = 0;
      pCVar2 = (CDuiString *)(**(code **)(**(int **)((int)this + 0x974) + 0x28))();
      local_8._0_1_ = 1;
      DuiLib::CDuiString::operator=(local_98,pCVar2);
      local_8 = (uint)local_8._1_3_ << 8;
      DuiLib::CDuiString::~CDuiString(local_11c);
      pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_((CDuiString *)((int)this + 0x8d8));
      iVar4 = DuiLib::CDuiString::CompareNoCase(local_98,pwVar3);
      if (iVar4 == 0) {
        DuiLib::CWindowWnd::Close((CWindowWnd *)((int)this + -0x20),0);
        DuiLib::CDuiString::~CDuiString(local_98);
      }
      else {
        bVar1 = DuiLib::CDuiString::IsEmpty(local_98);
        if (bVar1) {
          memset(local_91c,0,0x884);
          FUN_0041c1c0((WindowImplBase *)local_91c);
          local_8 = CONCAT31(local_8._1_3_,2);
          DuiLib::CDuiString::operator=(local_1a0,L"warning_title_text");
          DuiLib::CDuiString::operator=(local_11c,L"no_name_text");
          DuiLib::CWindowWnd::Create
                    ((CWindowWnd *)local_91c,*(HWND__ **)((int)this + -0x1c),L"MsgWnd",0x90000000,
                     0x80,0,0,800,800,(HMENU__ *)0x0);
          DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_91c);
          DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_91c);
          local_91c[0] = CMsgWnd::vftable;
          local_90c = CMsgWnd::vftable;
          local_8fc = CMsgWnd::vftable;
          local_8f8 = CMsgWnd::vftable;
          local_8f4 = CMsgWnd::vftable;
          local_8f0 = CMsgWnd::vftable;
          DuiLib::CDuiString::~CDuiString(local_11c);
          DuiLib::CDuiString::~CDuiString(local_1a0);
          DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_91c);
          DuiLib::CDuiString::~CDuiString(local_98);
        }
        else {
          if ((*(int *)((int)this + 0x95c) == 0) || (*(int *)((int)this + 0x95c) == 2)) {
            DuiLib::CDuiString::CDuiString(aCStack_9b5 + -3,local_98);
            iVar4 = FUN_00403140(*(int **)((int)this + 0x850),in_stack_fffff648);
            if (iVar4 != 0) {
              memset(local_91c,0,0x884);
              FUN_0041c1c0((WindowImplBase *)local_91c);
              local_8 = CONCAT31(local_8._1_3_,3);
              DuiLib::CDuiString::operator=(local_1a0,L"warning_title_text");
              DuiLib::CDuiString::operator=(local_11c,L"same_macro_dir_text");
              DuiLib::CWindowWnd::Create
                        ((CWindowWnd *)local_91c,*(HWND__ **)((int)this + -0x1c),L"MsgWnd",
                         0x90000000,0x80,0,0,800,800,(HMENU__ *)0x0);
              DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_91c);
              DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_91c);
              local_91c[0] = CMsgWnd::vftable;
              local_90c = CMsgWnd::vftable;
              local_8fc = CMsgWnd::vftable;
              local_8f8 = CMsgWnd::vftable;
              local_8f4 = CMsgWnd::vftable;
              local_8f0 = CMsgWnd::vftable;
              DuiLib::CDuiString::~CDuiString(local_11c);
              DuiLib::CDuiString::~CDuiString(local_1a0);
              DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_91c);
              DuiLib::CDuiString::~CDuiString(local_98);
              ExceptionList = local_10;
              return;
            }
          }
          else {
            DuiLib::CDuiString::CDuiString(aCStack_9b5 + -3,local_98);
            local_8._0_1_ = 4;
            DuiLib::CDuiString::CDuiString(aCStack_a39 + -3,(CDuiString *)((int)this + 0x854));
            local_8 = (uint)local_8._1_3_ << 8;
            iVar4 = FUN_00403220(*(int **)((int)this + 0x850),in_stack_fffff5c4);
            if (iVar4 != 0) {
              memset(local_91c,0,0x884);
              FUN_0041c1c0((WindowImplBase *)local_91c);
              local_8 = CONCAT31(local_8._1_3_,5);
              DuiLib::CDuiString::operator=(local_1a0,L"warning_title_text");
              DuiLib::CDuiString::operator=(local_11c,L"same_macro_text");
              DuiLib::CWindowWnd::Create
                        ((CWindowWnd *)local_91c,*(HWND__ **)((int)this + -0x1c),L"MsgWnd",
                         0x90000000,0x80,0,0,800,800,(HMENU__ *)0x0);
              DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_91c);
              DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_91c);
              local_91c[0] = CMsgWnd::vftable;
              local_90c = CMsgWnd::vftable;
              local_8fc = CMsgWnd::vftable;
              local_8f8 = CMsgWnd::vftable;
              local_8f4 = CMsgWnd::vftable;
              local_8f0 = CMsgWnd::vftable;
              DuiLib::CDuiString::~CDuiString(local_11c);
              DuiLib::CDuiString::~CDuiString(local_1a0);
              DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_91c);
              DuiLib::CDuiString::~CDuiString(local_98);
              ExceptionList = local_10;
              return;
            }
          }
          DuiLib::CDuiString::operator=((CDuiString *)((int)this + 0x8d8),local_98);
          DuiLib::CWindowWnd::Close((CWindowWnd *)((int)this + -0x20),1);
          DuiLib::CDuiString::~CDuiString(local_98);
        }
      }
    }
    else if ((iVar4 == *(int *)((int)this + 0x968)) || (iVar4 == *(int *)((int)this + 0x964))) {
      DuiLib::CWindowWnd::Close((CWindowWnd *)((int)this + -0x20),0);
    }
  }
  ExceptionList = local_10;
  return;
}


