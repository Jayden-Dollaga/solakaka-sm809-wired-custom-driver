// Program: SM809 mouse Software.exe
// Function: FUN_0040b3b0
// Entry: 0040b3b0
// Body: 0040b3b0 - 0040b643
// Signature: undefined FUN_0040b3b0(void * param_1)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void __fastcall FUN_0040b3b0(void *param_1)

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
  puStack_c = &LAB_00421e90;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  iVar1 = (**(code **)(*(int *)(*(int *)((int)param_1 + 0x684) + 0x6c8) + 8))(local_14);
  if (-1 < iVar1) {
    pCVar2 = DuiLib::CPaintManagerUI::FindControl
                       (*(CPaintManagerUI **)((int)param_1 + 0x10),L"disable_window_ver");
    (**(code **)(*(int *)pCVar2 + 0xf8))(1);
    memset(local_898,0,0x884);
    FUN_0041c1c0((WindowImplBase *)local_898);
    local_8 = 0;
    DuiLib::CDuiString::operator=(local_11c,L"warning_title_text");
    DuiLib::CDuiString::operator=(local_98,L"delete_gun_text");
    DuiLib::CWindowWnd::Create
              ((CWindowWnd *)local_898,*(HWND__ **)((int)param_1 + 0x14),L"MsgWnd",0x90000000,0x80,0
               ,0,800,800,(HMENU__ *)0x0);
    DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)local_898);
    uVar3 = DuiLib::CWindowWnd::ShowModal((CWindowWnd *)local_898);
    if (uVar3 == 1) {
      (**(code **)(*(int *)pCVar2 + 0xf8))(0);
      this = (CStdPtrArray *)((int)param_1 + 400);
      pvVar4 = DuiLib::CStdPtrArray::operator[](this,iVar1);
      if (DAT_0046c398 != DAT_0046c39c) {
        _Dst = (void *)(DAT_0046c398 + (int)pvVar4 * 4);
        pvVar6 = (void *)((int)_Dst + 4);
        memmove(_Dst,pvVar6,DAT_0046c39c - (int)pvVar6);
        DAT_0046c39c = DAT_0046c39c + -4;
        FUN_00403350();
      }
      uVar8 = 0x40b521;
      (**(code **)(*(int *)(*(int *)((int)param_1 + 0x684) + 0x558) + 0x1c))(iVar1);
      iVar5 = DuiLib::CStdPtrArray::GetSize(this);
      iVar7 = iVar1;
      if (iVar1 < iVar5) {
        do {
          pvVar6 = DuiLib::CStdPtrArray::operator[](this,iVar7);
          uVar8 = 0x40b544;
          DuiLib::CStdPtrArray::SetAt(this,iVar7,(void *)((int)pvVar6 + -1));
          iVar7 = iVar7 + 1;
          iVar5 = DuiLib::CStdPtrArray::GetSize(this);
        } while (iVar7 < iVar5);
      }
      uVar9 = 0x40b560;
      DuiLib::CStdPtrArray::Remove(this,iVar1);
      iVar7 = FUN_00404200((uint)pvVar4,DAT_00432aa8,uVar8,uVar9,1);
      if (iVar7 != 0) {
        SendMessageW(*(HWND *)((int)param_1 + 0x14),0x467,0,0);
      }
      if ((DAT_0046c39c - DAT_0046c398 >> 2 <= iVar1) && (iVar1 + -1 < 0)) {
        FUN_0040b650(param_1,0xffffffff);
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


