// Program: Hook.dll
// Function: __amsg_exit
// Entry: 100016a8
// Body: 100016a8 - 100016d7
// Signature: void __amsg_exit(int param_1)


/* Library Function - Single Match
    __amsg_exit
   
   Library: Visual Studio 2003 Release */

void __cdecl __amsg_exit(int param_1)

{
  if ((DAT_10007d3c == 1) || ((DAT_10007d3c == 0 && (DAT_10007d40 == 1)))) {
    FUN_100029a0();
  }
  FUN_100029d9(param_1);
  (*(code *)PTR___exit_10007074)(0xff);
  return;
}


