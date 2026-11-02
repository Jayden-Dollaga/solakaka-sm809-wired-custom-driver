// Program: MSDriver.dll
// Function: FUN_10004cab
// Entry: 10004cab
// Body: 10004cab - 10004d03
// Signature: int FUN_10004cab(LPSTR param_1, WCHAR param_2)


int __cdecl FUN_10004cab(LPSTR param_1,WCHAR param_2)

{
  int iVar1;
  bool bVar2;
  
  InterlockedIncrement((LONG *)&DAT_1000a254);
  bVar2 = DAT_1000a250 != 0;
  if (bVar2) {
    InterlockedDecrement((LONG *)&DAT_1000a254);
    FUN_1000277c(0x13);
  }
  iVar1 = FUN_10004d04(param_1,param_2);
  if (bVar2) {
    FUN_100027dd(0x13);
  }
  else {
    InterlockedDecrement((LONG *)&DAT_1000a254);
  }
  return iVar1;
}


