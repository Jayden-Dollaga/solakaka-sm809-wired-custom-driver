// Program: SM809 mouse Software.exe
// Function: FUN_00410690
// Entry: 00410690
// Body: 00410690 - 00410985
// Signature: undefined FUN_00410690(void * param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_00410690(void *param_1)

{
  CStdPtrArray *this;
  void *_Dst;
  int iVar1;
  CControlUI *pCVar2;
  uint uVar3;
  void *pvVar4;
  int iVar5;
  void *pvVar6;
  int iVar7;
  undefined4 uVar8;
  undefined4 uVar9;
  undefined **local_898 [4];
  undefined **local_888;
  undefined **local_878;
  undefined **local_874;
  undefined **local_870;
  undefined **local_86c;
  CDuiString local_11c [132];
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_00422870;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  iVar1 = (**(code **)(*(int *)(*(int *)((int)param_1 + 0x398) + 0x6c8) + 8))(local_14);
  if (-1 < iVar1) {
    pCVar2 = DuiLib::CPaintManagerUI::FindControl
                       (*(CPaintManagerUI **)((int)param_1 + 0x10),L"disable_window_ver");
    (**(code **)(*(int *)pCVar2 + 0xf8))(1);
    memset(local_898,0,0x884);
    FUN_0041c1c0((WindowImplBase *)local_898);
    local_8 = 0;
    DuiLib::CDuiString::operator=(local_11c,L"warning_title_text");
    DuiLib::CDuiString::operator=(local_98,L"delete_macro_text");
    uVar8 = 0;
    DuiLib::CWindowWnd::Create
              ((CWindowWnd *)local_898,*(HWND__ **)((int)param_1 + 0x14),L"MsgWnd",0x90000000,0x80,0
               ,0,800,800,(HMENU__ *)0x0);
    DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_898);
    uVar3 = DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_898);
    if (uVar3 == 1) {
      (**(code **)(*(int *)pCVar2 + 0xf8))(0);
      this = (CStdPtrArray *)((int)param_1 + 0x2f8);
      pvVar4 = DuiLib::CStdPtrArray::operator[](this,iVar1);
      if (DAT_0046c380 != DAT_0046c384) {
        _Dst = (void *)(DAT_0046c380 + (int)pvVar4 * 4);
        pvVar6 = (void *)((int)_Dst + 4);
        uVar8 = 0x4107e0;
        memmove(_Dst,pvVar6,DAT_0046c384 - (int)pvVar6);
        DAT_0046c384 = DAT_0046c384 + -4;
        FUN_00402ef0();
      }
      (**(code **)(*(int *)(*(int *)((int)param_1 + 0x398) + 0x558) + 0x1c))(iVar1);
      iVar5 = DuiLib::CStdPtrArray::GetSize(this);
      iVar7 = iVar1;
      if (iVar1 < iVar5) {
        do {
          pvVar6 = DuiLib::CStdPtrArray::operator[](this,iVar7);
          uVar8 = 0x410824;
          DuiLib::CStdPtrArray::SetAt(this,iVar7,(void *)((int)pvVar6 + -1));
          iVar7 = iVar7 + 1;
          iVar5 = DuiLib::CStdPtrArray::GetSize(this);
        } while (iVar7 < iVar5);
      }
      uVar9 = 0x410840;
      DuiLib::CStdPtrArray::Remove(this,iVar1);
      iVar7 = FUN_004040e0((uint)pvVar4,DAT_00432aa8,uVar8,uVar9,1);
      if (iVar7 != 0) {
        SendMessageW(*(HWND *)((int)param_1 + 0x14),0x467,0,0);
      }
      iVar7 = (**(code **)(*(int *)(*(int *)((int)param_1 + 0x398) + 0x558) + 0xc))();
      if ((iVar7 <= iVar1) && (iVar1 + -1 < 0)) {
        *(undefined4 *)((int)param_1 + 0x2c0) = 0;
        memset((void *)((int)param_1 + 0x24),0,0x280);
        *(undefined4 *)((int)param_1 + 0x2a4) = 0;
        *(undefined4 *)((int)param_1 + 700) = 0xffffffff;
        FUN_00411740(param_1,-1);
        (**(code **)(**(int **)((int)param_1 + 0x348) + 0x2c))(&DAT_0042628c);
        (**(code **)(**(int **)((int)param_1 + 0x388) + 0x2c))(&DAT_00427820);
        *(undefined4 *)((int)param_1 + 0x1c) = 0;
        FUN_00411220((int)param_1);
        *(undefined4 *)((int)param_1 + 0x1c) = 0;
      }
    }
    (**(code **)(*(int *)pCVar2 + 0xf8))(0);
    local_898[0] = CMsgWnd::vftable;
    local_888 = CMsgWnd::vftable;
    local_878 = CMsgWnd::vftable;
    local_874 = CMsgWnd::vftable;
    local_870 = CMsgWnd::vftable;
    local_86c = CMsgWnd::vftable;
    DuiLib::CDuiString::~CDuiString(local_98);
    DuiLib::CDuiString::~CDuiString(local_11c);
    DuiLib::WindowImplBase::~WindowImplBase((WindowImplBase *)local_898);
  }
  ExceptionList = local_10;
  return;
}


