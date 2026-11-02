// Program: MSDriver.dll
// Function: FUN_10001c00
// Entry: 10001c00
// Body: 10001c00 - 10001de4
// Signature: uint FUN_10001c00(LPCSTR param_1, undefined4 * param_2, int param_3)


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

uint __cdecl FUN_10001c00(LPCSTR param_1,undefined4 *param_2,int param_3)

{
  undefined4 *puVar1;
  short *psVar2;
  char cVar3;
  HANDLE pvVar4;
  uint uVar5;
  int iVar6;
  undefined4 uVar7;
  
  pvVar4 = CreateFileA(param_1,0xc0000000,3,(LPSECURITY_ATTRIBUTES)0x0,3,0x40000000,(HANDLE)0x0);
  *param_2 = pvVar4;
  if (pvVar4 != (HANDLE)0xffffffff) {
    puVar1 = param_2 + 1;
    cVar3 = HidD_GetPreparsedData(pvVar4,puVar1);
    if (cVar3 == '\0') {
      uVar5 = CloseHandle((HANDLE)*param_2);
      *param_2 = 0;
      return uVar5 & 0xffffff00;
    }
    cVar3 = HidD_GetAttributes(*param_2,param_2 + 0x12);
    if (cVar3 != '\0') {
      psVar2 = (short *)(param_2 + 2);
      iVar6 = HidP_GetCaps(*puVar1,psVar2);
      if (iVar6 != 0) {
        if (param_3 == 0) {
          if (((*(short *)((int)param_2 + 10) == -0xff) && (*psVar2 == -0xff)) &&
             ((*(ushort *)(param_2 + 0x13) == DAT_10009de4 &&
              (*(ushort *)((int)param_2 + 0x4e) == DAT_10009de0)))) {
            OutputDebugStringA(s_OpenHidDevice_Success_10009108);
            uVar7 = FUN_10002260((int)param_2);
            return CONCAT31((int3)((uint)uVar7 >> 8),1);
          }
        }
        else {
          if (param_3 == 1) {
            if (((*(short *)((int)param_2 + 10) == -1) && (*psVar2 == 0xff)) &&
               ((*(ushort *)(param_2 + 0x13) == DAT_10009de4 &&
                (*(ushort *)((int)param_2 + 0x4e) == DAT_10009de0)))) {
              OutputDebugStringA(s_OpenFeatureDevice_Success_100090ec);
              _DAT_10009ee8 = *param_2;
              *param_2 = 0;
              uVar7 = HidD_FreePreparsedData(*puVar1);
              return CONCAT31((int3)((uint)uVar7 >> 8),1);
            }
            CloseHandle((HANDLE)*param_2);
            *param_2 = 0;
            uVar5 = HidD_FreePreparsedData(*puVar1);
            return uVar5 & 0xffffff00;
          }
          if (param_3 != 2) {
            return CONCAT31((int3)((uint)param_3 >> 8),param_1._0_1_);
          }
          if ((((*(short *)((int)param_2 + 10) == -0x100) && (*psVar2 == -0x100)) &&
              (*(ushort *)(param_2 + 0x13) == DAT_10009de4)) &&
             (*(ushort *)((int)param_2 + 0x4e) == DAT_10009de0)) {
            OutputDebugStringA(s_OpenHidDevice_Success_10009108);
            uVar7 = FUN_10002260((int)param_2);
            return CONCAT31((int3)((uint)uVar7 >> 8),1);
          }
        }
        HidD_FreePreparsedData(*puVar1);
        uVar5 = CloseHandle((HANDLE)*param_2);
        *param_2 = 0;
        return uVar5 & 0xffffff00;
      }
    }
    HidD_FreePreparsedData(*puVar1);
    pvVar4 = (HANDLE)CloseHandle((HANDLE)*param_2);
  }
  *param_2 = 0;
  return (uint)pvVar4 & 0xffffff00;
}


