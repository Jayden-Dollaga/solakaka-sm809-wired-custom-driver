// Program: SM809 mouse Software.exe
// Function: FUN_00405b80
// Entry: 00405b80
// Body: 00405b80 - 00405baa
// Signature: undefined FUN_00405b80(undefined4 param_1, undefined4 param_2, undefined1 param_3)


void __cdecl FUN_00405b80(undefined4 param_1,undefined4 param_2,undefined1 param_3)

{
  uint *puVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  undefined1 *puVar4;
  
  puVar4 = &param_3;
  uVar3 = 0;
  uVar2 = 0xffffffff;
  puVar1 = (uint *)FUN_00405b70();
  __stdio_common_vswscanf(*puVar1 | 1,puVar1[1],param_1,uVar2,param_2,uVar3,puVar4);
  return;
}


