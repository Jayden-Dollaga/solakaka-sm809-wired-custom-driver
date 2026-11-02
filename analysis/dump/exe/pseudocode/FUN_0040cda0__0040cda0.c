// Program: SM809 mouse Software.exe
// Function: FUN_0040cda0
// Entry: 0040cda0
// Body: 0040cda0 - 0040d0e6
// Signature: undefined FUN_0040cda0(void * param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_0040cda0(void *param_1)

{
  uint uVar1;
  int iVar2;
  CDuiString *this;
  wchar_t *pwVar3;
  int iVar4;
  undefined4 *puVar5;
  code *pcVar6;
  void *pvVar7;
  CDuiString local_a34 [132];
  CControlUI *local_9b0;
  undefined **local_9ac [4];
  undefined **local_99c;
  undefined **local_98c;
  undefined **local_988;
  undefined **local_984;
  undefined **local_980;
  CDuiString local_230 [132];
  CDuiString local_1ac [132];
  CDuiString local_128 [132];
  CDuiString local_a4 [132];
  CStdPtrArray local_20 [12];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_004221ed;
  local_10 = ExceptionList;
  uVar1 = DAT_00432008 ^ (uint)(local_20 + 0x1c);
  ExceptionList = &local_10;
  local_14 = uVar1;
  iVar2 = DuiLib::CStdPtrArray::GetSize((CStdPtrArray *)((int)param_1 + 0x19c));
  if ((0 < iVar2) && (-1 < *(int *)((int)param_1 + 0x1a8))) {
    local_9b0 = DuiLib::CPaintManagerUI::FindControl
                          (*(CPaintManagerUI **)((int)param_1 + 0x10),L"disable_window_ver");
    (**(code **)(*(int *)local_9b0 + 0xf8))(1,uVar1);
    memset(local_9ac,0,0x884);
    FUN_0041c1c0((WindowImplBase *)local_9ac);
    local_8 = 0;
    DuiLib::CDuiString::operator=(local_230,L"warning_title_text");
    DuiLib::CDuiString::operator=(local_1ac,L"delete_gun_dir_text");
    DuiLib::CWindowWnd::Create
              ((CWindowWnd *)local_9ac,*(HWND__ **)((int)param_1 + 0x14),L"MsgWnd",0x90000000,0x80,0
               ,0,800,800,(HMENU__ *)0x0);
    DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_9ac);
    uVar1 = DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_9ac);
    pcVar6 = ~CDuiString_exref;
    if (uVar1 == 1) {
      DuiLib::CDuiString::CDuiString(local_128);
      local_8._0_1_ = 1;
      this = DuiLib::CStdPtrArray::operator[]
                       ((CStdPtrArray *)((int)param_1 + 0x19c),*(int *)((int)param_1 + 0x1a8));
      pwVar3 = DuiLib::CDuiString::GetData(this);
      DuiLib::CDuiString::operator=(local_128,pwVar3);
      DuiLib::CDuiString::CDuiString(local_a34,local_128);
      local_8._0_1_ = 2;
      DuiLib::CDuiString::CDuiString(local_a4);
      pvVar7 = (void *)0x0;
      local_8._0_1_ = 3;
      DuiLib::CStdPtrArray::CStdPtrArray(local_20,0);
      local_8 = CONCAT31(local_8._1_3_,4);
      DuiLib::CStdPtrArray::Empty(local_20);
      puVar5 = DAT_0046c398;
      if (DAT_0046c398 != DAT_0046c39c) {
        do {
          DuiLib::CDuiString::operator=(local_a4,(wchar_t *)*puVar5);
          pwVar3 = DuiLib::CDuiString::operator_wchar_t_const_(local_a34);
          iVar2 = DuiLib::CDuiString::CompareNoCase(local_a4,pwVar3);
          if (iVar2 == 0) {
            DuiLib::CStdPtrArray::Add(local_20,pvVar7);
          }
          puVar5 = puVar5 + 1;
          pvVar7 = (void *)((int)pvVar7 + 1);
        } while (puVar5 != DAT_0046c39c);
      }
      iVar2 = DuiLib::CStdPtrArray::GetSize(local_20);
      while (iVar2 = iVar2 + -1, -1 < iVar2) {
        pvVar7 = DuiLib::CStdPtrArray::GetAt(local_20,iVar2);
        puVar5 = DAT_0046c398 + (int)pvVar7;
        memmove(puVar5,puVar5 + 1,(int)DAT_0046c39c - (int)(puVar5 + 1));
        DAT_0046c39c = DAT_0046c39c + -1;
      }
      FUN_00403350();
      DuiLib::CStdPtrArray::~CStdPtrArray(local_20);
      pcVar6 = ~CDuiString_exref;
      DuiLib::CDuiString::~CDuiString(local_a4);
      local_8 = CONCAT31(local_8._1_3_,1);
      DuiLib::CDuiString::~CDuiString(local_a34);
      DuiLib::CStdPtrArray::Remove
                ((CStdPtrArray *)((int)param_1 + 0x19c),*(int *)((int)param_1 + 0x1a8));
      (**(code **)(*(int *)(*(int *)((int)param_1 + 0x1b0) + 0x558) + 0x1c))
                (*(undefined4 *)((int)param_1 + 0x1a8));
      iVar4 = DuiLib::CStdPtrArray::GetSize((CStdPtrArray *)((int)param_1 + 0x19c));
      iVar2 = *(int *)((int)param_1 + 0x1a8);
      if (iVar4 <= iVar2) {
        iVar2 = iVar2 + -1;
        *(int *)((int)param_1 + 0x1a8) = iVar2;
      }
      if (iVar2 < 0) {
        DuiLib::CStdPtrArray::Empty((CStdPtrArray *)((int)param_1 + 400));
        (**(code **)(*(int *)(*(int *)((int)param_1 + 0x684) + 0x558) + 0x20))();
        FUN_0040b650(param_1,0xffffffff);
        *(undefined4 *)((int)param_1 + 0x1c) = 0;
      }
      local_8 = local_8 & 0xffffff00;
      DuiLib::CDuiString::~CDuiString(local_128);
    }
    (**(code **)(*(int *)local_9b0 + 0xf8))(0);
    local_9ac[0] = CMsgWnd::vftable;
    local_99c = CMsgWnd::vftable;
    local_98c = CMsgWnd::vftable;
    local_988 = CMsgWnd::vftable;
    local_984 = CMsgWnd::vftable;
    local_980 = CMsgWnd::vftable;
    (*pcVar6)();
    (*pcVar6)();
    DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_9ac);
  }
  ExceptionList = local_10;
  return;
}


