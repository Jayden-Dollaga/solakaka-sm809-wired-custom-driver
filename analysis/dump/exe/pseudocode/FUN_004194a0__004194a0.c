// Program: SM809 mouse Software.exe
// Function: FUN_004194a0
// Entry: 004194a0
// Body: 004194a0 - 00419596
// Signature: undefined FUN_004194a0(void * this, uint param_1)


void __thiscall FUN_004194a0(void *this,uint param_1)

{
  int iVar1;
  uint uVar2;
  uint uVar3;
  uint uVar4;
  bool bVar5;
  bool bVar6;
  
  uVar4 = param_1 >> 0x10;
  uVar3 = param_1 & 0xffff;
  if (uVar4 == 0x7f00) {
    if (uVar3 == 1) {
      if (DAT_00432aa4 != 1) {
        Sleep(500);
        DAT_00432aa4 = 1;
        (**(code **)((int)this + 0x780))();
        iVar1 = (**(code **)((int)this + 0x790))();
        if (iVar1 != 0) {
          *(undefined4 *)((int)this + 0x16d0) = 1;
          FUN_004196b0((int)this);
          FUN_0041bbc0((int)this);
          return;
        }
      }
    }
    else if ((uVar3 == 2) && (DAT_00432aa4 != 2)) {
      DAT_00432aa4 = uVar3;
      (**(code **)((int)this + 0x784))();
      (**(code **)((int)this + 0x794))();
      *(undefined4 *)((int)this + 0x16d0) = 0;
      ShowWindow(*(HWND *)((int)this + 4),0);
      return;
    }
  }
  else {
    uVar2 = uVar4 & 0xff00;
    if (uVar2 == 0x700) {
      bVar5 = uVar3 - 1 < 7;
      bVar6 = uVar3 - 1 == 7;
    }
    else if (uVar2 == 0x500) {
      bVar5 = uVar3 - 1 < 7;
      bVar6 = uVar3 - 1 == 7;
    }
    else {
      if (uVar2 != 0x800) {
        return;
      }
      bVar5 = uVar3 == 1;
      bVar6 = uVar3 == 2;
    }
    if (bVar5 || bVar6) {
      FUN_004195a0(this,uVar4,uVar3);
    }
  }
  return;
}


