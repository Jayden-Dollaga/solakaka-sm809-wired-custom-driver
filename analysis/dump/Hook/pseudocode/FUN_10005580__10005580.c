// Program: Hook.dll
// Function: FUN_10005580
// Entry: 10005580
// Body: 10005580 - 100055ae
// Signature: undefined FUN_10005580(undefined1 param_1)


/* WARNING: Unable to track spacebase fully for stack */

void __cdecl FUN_10005580(undefined1 param_1)

{
  uint in_EAX;
  undefined1 *puVar1;
  undefined4 unaff_retaddr;
  
  puVar1 = &param_1;
  for (; 0xfff < in_EAX; in_EAX = in_EAX - 0x1000) {
    puVar1 = puVar1 + -0x1000;
  }
  *(undefined4 *)(puVar1 + (-4 - in_EAX)) = unaff_retaddr;
  return;
}


