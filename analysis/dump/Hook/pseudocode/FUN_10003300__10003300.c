// Program: Hook.dll
// Function: FUN_10003300
// Entry: 10003300
// Body: 10003300 - 1000338c
// Signature: int * FUN_10003300(int param_1, int param_2)


int * __cdecl FUN_10003300(int param_1,int param_2)

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
      if (_Size <= DAT_10007840) {
        FUN_1000328a(9);
        piVar1 = FUN_10004029(_Size);
        FUN_100032eb(9);
        if (piVar1 != (int *)0x0) {
          _memset(piVar1,0,(size_t)_Size);
          return piVar1;
        }
      }
      piVar1 = HeapAlloc(DAT_100092e4,8,(SIZE_T)puVar3);
      if (piVar1 != (int *)0x0) {
        return piVar1;
      }
    }
    if (DAT_10007f38 == 0) {
      return (int *)0x0;
    }
    iVar2 = FUN_10004a58(puVar3);
  } while (iVar2 != 0);
  return (int *)0x0;
}


