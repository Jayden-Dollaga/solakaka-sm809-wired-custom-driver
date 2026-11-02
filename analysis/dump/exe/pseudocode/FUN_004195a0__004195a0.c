// Program: SM809 mouse Software.exe
// Function: FUN_004195a0
// Entry: 004195a0
// Body: 004195a0 - 004196a8
// Signature: undefined FUN_004195a0(void * this, uint param_1, int param_2)


void __thiscall FUN_004195a0(void *this,uint param_1,int param_2)

{
  uint uVar1;
  int iVar2;
  
  uVar1 = param_1 & 0xff00;
  if (uVar1 == 0x700) {
    if (param_2 - 1U < 8) {
      iVar2 = param_2 + -1;
      *(int *)(DAT_00432aa0 + 0x84) = iVar2;
      (**(code **)(**(int **)((int)this + iVar2 * 4 + 0x988) + 0x1bc))(1,1);
      PostMessageW(*(HWND *)((int)this + 4),0x469,0,*(LPARAM *)(DAT_00432aa0 + 0x88 + iVar2 * 4));
      FUN_004035a0();
      return;
    }
  }
  else if (uVar1 == 0x500) {
    if (param_2 - 1U < 8) {
      if (param_2 == 8) {
        param_2 = 0;
      }
      else if (param_2 == 4) {
        param_2 = 1;
      }
      else if ((param_2 != 2) && (param_2 == 1)) {
        param_2 = 3;
      }
      *(int *)(DAT_00432aa0 + 0x80) = param_2;
      (**(code **)(**(int **)((int)this + param_2 * 4 + 0x978) + 0x1bc))(1,1);
      FUN_004035a0();
      return;
    }
  }
  else if ((uVar1 == 0x800) && (param_2 - 1U < 2)) {
    *(int *)(DAT_00432aa0 + 0x14c) = param_2 + -1;
    FUN_00408bc0((void *)((int)this + 0x7a0),param_2 + -1);
    FUN_004035a0();
  }
  return;
}


