// Program: MSDriver.dll
// Function: __amsg_exit
// Entry: 10002603
// Body: 10002603 - 10002632
// Signature: void __amsg_exit(int param_1)


/* Library Function - Single Match
    __amsg_exit
   
   Library: Visual Studio 2003 Release */

void __cdecl __amsg_exit(int param_1)

{
  if ((DAT_10009f08 == 1) || ((DAT_10009f08 == 0 && (DAT_10009f0c == 1)))) {
    FUN_100042c7();
  }
  FUN_10004300(param_1);
  (*(code *)PTR___exit_10009144)(0xff);
  return;
}


