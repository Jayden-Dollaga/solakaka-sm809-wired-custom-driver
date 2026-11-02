// Program: SM809 mouse Software.exe
// Function: FUN_00408bc0
// Entry: 00408bc0
// Body: 00408bc0 - 00408c50
// Signature: undefined FUN_00408bc0(void * this, int param_1)


void __thiscall FUN_00408bc0(void *this,int param_1)

{
  if (param_1 != 0) {
    (**(code **)(**(int **)((int)this + 0x128) + 0xf8))(0);
    (**(code **)(**(int **)((int)this + 300) + 0xf8))(0);
    (**(code **)(**(int **)((int)this + 0x130) + 0xf8))(1);
  }
  else {
    (**(code **)(**(int **)((int)this + 0x128) + 0xf8))(1);
    (**(code **)(**(int **)((int)this + 300) + 0xf8))(1);
    (**(code **)(**(int **)((int)this + 0x130) + 0xf8))(0);
  }
  (**(code **)(**(int **)((int)this + 0x134) + 0xf8))(param_1 != 0);
  (**(code **)(**(int **)((int)this + param_1 * 4 + 0x120) + 0x1bc))(1,1);
  return;
}


