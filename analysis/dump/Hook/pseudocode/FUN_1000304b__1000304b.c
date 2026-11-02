// Program: Hook.dll
// Function: FUN_1000304b
// Entry: 1000304b
// Body: 1000304b - 100030a3
// Signature: int FUN_1000304b(LPSTR param_1, WCHAR param_2)


int __cdecl FUN_1000304b(LPSTR param_1,WCHAR param_2)

{
  int iVar1;
  bool bVar2;
  
  InterlockedIncrement((LONG *)&DAT_10008084);
  bVar2 = DAT_10008080 != 0;
  if (bVar2) {
    InterlockedDecrement((LONG *)&DAT_10008084);
    FUN_1000328a(0x13);
  }
  iVar1 = FUN_100030a4(param_1,param_2);
  if (bVar2) {
    FUN_100032eb(0x13);
  }
  else {
    InterlockedDecrement((LONG *)&DAT_10008084);
  }
  return iVar1;
}


