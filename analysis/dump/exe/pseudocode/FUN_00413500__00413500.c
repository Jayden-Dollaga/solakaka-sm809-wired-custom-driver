// Program: SM809 mouse Software.exe
// Function: FUN_00413500
// Entry: 00413500
// Body: 00413500 - 004135b7
// Signature: undefined FUN_00413500(int param_1, CDuiString param_2)


void __thiscall FUN_00413500(int param_1,CDuiString param_2)

{
  uint uVar1;
  CListLabelElementUI *this;
  wchar_t *pwVar2;
  int in_stack_00000088;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  puStack_c = &LAB_00422190;
  local_10 = ExceptionList;
  uVar1 = DAT_00432008 ^ (int)register0x00000010 - 4U;
  ExceptionList = &local_10;
  local_8 = 0;
  this = operator_new(0x570);
  local_8._0_1_ = 1;
  DuiLib::CListLabelElementUI::CListLabelElementUI(this);
  *(undefined ***)this = DuiLib::CListLabelElementUI::vftable;
  local_8 = (uint)local_8._1_3_ << 8;
  pwVar2 = DuiLib::CDuiString::operator_wchar_t_const_(&param_2);
  DuiLib::CControlUI::SetText((CControlUI *)this,pwVar2);
  (**(code **)(*(int *)this + 0x88))(0x1e,uVar1);
  if (in_stack_00000088 != 0) {
    DuiLib::CControlUI::SetBkImage
              ((CControlUI *)this,L"res=\'skins/lock.png\' dest=\'250,0,280,30\'");
  }
  (**(code **)(*(int *)(*(int *)(param_1 + 0x398) + 0x558) + 0x10))(this);
  DuiLib::CDuiString::~CDuiString(&param_2);
  ExceptionList = local_10;
  return;
}


