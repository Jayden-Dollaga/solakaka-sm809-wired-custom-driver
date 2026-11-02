// Program: MSDriver.dll
// Function: FUN_10002322
// Entry: 10002322
// Body: 10002322 - 100023ae
// Signature: int * FUN_10002322(int param_1, int param_2)


int * __cdecl FUN_10002322(int param_1,int param_2)

{
  int *piVar1;
  int iVar2;
  uint *_Size;
  uint *puVar3;
  
  _Size = (uint *)(param_1 * param_2);
  puVar3 = _Size;
  if (_Size < (uint *)0xffffffe1) {
    if (_Size == (uint *)0x0) {
      puVar3 = (uint *)0x1;
    }
    puVar3 = (uint *)((int)puVar3 + 0xfU & 0xfffffff0);
  }
  do {
    if (puVar3 < (uint *)0xffffffe1) {
      if (_Size <= DAT_1000920c) {
        FUN_1000277c(9);
        piVar1 = FUN_10002b86(_Size);
        FUN_100027dd(9);
        if (piVar1 != (int *)0x0) {
          _memset(piVar1,0,(size_t)_Size);
          return piVar1;
        }
      }
      piVar1 = HeapAlloc(DAT_1000b5f0,8,(SIZE_T)puVar3);
      if (piVar1 != (int *)0x0) {
        return piVar1;
      }
    }
    if (DAT_10009f74 == 0) {
      return (int *)0x0;
    }
    iVar2 = FUN_10003098(puVar3);
  } while (iVar2 != 0);
  return (int *)0x0;
}


