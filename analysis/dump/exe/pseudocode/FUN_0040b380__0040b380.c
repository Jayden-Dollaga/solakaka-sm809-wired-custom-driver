// Program: SM809 mouse Software.exe
// Function: FUN_0040b380
// Entry: 0040b380
// Body: 0040b380 - 0040b3a6
// Signature: CListLabelElementUI * FUN_0040b380(void * this, byte param_1)


CListLabelElementUI * __thiscall FUN_0040b380(void *this,byte param_1)

{
  DuiLib::CListLabelElementUI::~CListLabelElementUI(this);
  if ((param_1 & 1) != 0) {
    FUN_0041feb7(this);
  }
  return this;
}


