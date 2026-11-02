// Program: MSDriver.dll
// Function: FUN_10006360
// Entry: 10006360
// Body: 10006360 - 1000638e
// Signature: undefined FUN_10006360(undefined1 param_1)


/* WARNING: Unable to track spacebase fully for stack */

void __cdecl FUN_10006360(undefined1 param_1)

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


