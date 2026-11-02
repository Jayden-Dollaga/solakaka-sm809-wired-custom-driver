// Program: SM809 mouse Software.exe
// Function: ___scrt_initialize_onexit_tables
// Entry: 0041ffc7
// Body: 0041ffc7 - 0042004d
// Signature: undefined4 ___scrt_initialize_onexit_tables(int param_1)


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* Library Function - Single Match
    ___scrt_initialize_onexit_tables
   
   Library: Visual Studio 2019 Release */

undefined4 __cdecl ___scrt_initialize_onexit_tables(int param_1)

{
  code *pcVar1;
  bool bVar2;
  undefined4 in_EAX;
  undefined3 extraout_var;
  int iVar3;
  uint uVar4;
  undefined4 uVar5;
  
  if (DAT_00432721 != '\0') {
    return CONCAT31((int3)((uint)in_EAX >> 8),1);
  }
  if ((param_1 != 0) && (param_1 != 1)) {
    FUN_004208e1();
    pcVar1 = (code *)swi(3);
    uVar5 = (*pcVar1)();
    return uVar5;
  }
  bVar2 = ___scrt_is_ucrt_dll_in_use();
  iVar3 = CONCAT31(extraout_var,bVar2);
  if ((iVar3 == 0) || (param_1 != 0)) {
    DAT_00432724 = 0xffffffff;
    _DAT_00432728 = 0xffffffff;
    _DAT_0043272c = 0xffffffff;
    _DAT_00432730 = 0xffffffff;
    _DAT_00432734 = 0xffffffff;
    _DAT_00432738 = 0xffffffff;
LAB_0042003a:
    DAT_00432721 = '\x01';
    uVar4 = CONCAT31((int3)((uint)iVar3 >> 8),1);
  }
  else {
    uVar4 = initialize_onexit_table(&DAT_00432724);
    if (uVar4 == 0) {
      uVar4 = initialize_onexit_table(&DAT_00432730);
      iVar3 = 0;
      if (uVar4 == 0) goto LAB_0042003a;
    }
    uVar4 = uVar4 & 0xffffff00;
  }
  return uVar4;
}


