// Program: SM809 mouse Software.exe
// Function: FUN_00404c40
// Entry: 00404c40
// Body: 00404c40 - 00404cea
// Signature: uint FUN_00404c40(void * this, uint param_1)


uint __thiscall FUN_00404c40(void *this,uint param_1)

{
  undefined1 *puVar1;
  uint uVar2;
  undefined1 *puVar3;
  int iVar4;
  
  uVar2 = **(uint **)((int)this + 0x1c);
  if (((uVar2 != 0) && (**(uint **)((int)this + 0xc) < uVar2)) &&
     ((param_1 == 0xffffffff || (*(byte *)(uVar2 - 1) == param_1)))) {
    **(int **)((int)this + 0x2c) = **(int **)((int)this + 0x2c) + 1;
    **(int **)((int)this + 0x1c) = **(int **)((int)this + 0x1c) + -1;
    if (param_1 == 0xffffffff) {
      param_1 = 0;
    }
    return param_1;
  }
  if ((*(FILE **)((int)this + 0x4c) != (FILE *)0x0) && (param_1 != 0xffffffff)) {
    if ((*(int *)((int)this + 0x38) == 0) &&
       (iVar4 = ungetc(param_1 & 0xff,*(FILE **)((int)this + 0x4c)), iVar4 != -1)) {
      return param_1;
    }
    puVar1 = (undefined1 *)((int)this + 0x3c);
    if ((undefined1 *)**(int **)((int)this + 0x1c) != puVar1) {
      *puVar1 = (char)param_1;
      puVar3 = (undefined1 *)**(int **)((int)this + 0xc);
      if (puVar3 != puVar1) {
        *(undefined1 **)((int)this + 0x50) = puVar3;
        *(int *)((int)this + 0x54) = **(int **)((int)this + 0x2c) + **(int **)((int)this + 0x1c);
      }
      **(int **)((int)this + 0xc) = (int)puVar1;
      **(int **)((int)this + 0x1c) = (int)puVar1;
      **(undefined4 **)((int)this + 0x2c) = 1;
      return param_1;
    }
  }
  return 0xffffffff;
}


