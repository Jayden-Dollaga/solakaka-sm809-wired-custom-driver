// Program: SM809 mouse Software.exe
// Function: FUN_00408c70
// Entry: 00408c70
// Body: 00408c70 - 00408e37
// Signature: undefined FUN_00408c70(void)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

void FUN_00408c70(void)

{
  int iVar1;
  HINSTANCE__ *pHVar2;
  HRSRC hResData;
  HGLOBAL hResData_00;
  DWORD DVar3;
  LPVOID pvVar4;
  CResourceManager *pCVar5;
  wchar_t *pwVar6;
  undefined *puVar7;
  wchar_t *lpType;
  HRSRC pHVar8;
  undefined4 uVar9;
  CDuiString local_98 [132];
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_004216e1;
  local_10 = ExceptionList;
  local_14 = DAT_00432008 ^ (uint)(local_98 + 0x94);
  ExceptionList = &local_10;
  DuiLib::CPaintManagerUI::SetResourceType(1);
  DuiLib::CPaintManagerUI::GetInstancePath();
  local_8 = 0;
  iVar1 = DuiLib::CPaintManagerUI::GetResourceType();
  switch(iVar1) {
  case 1:
    DuiLib::CDuiString::operator+=(local_98,L"res\\");
    pwVar6 = DuiLib::CDuiString::GetData(local_98);
    DuiLib::CPaintManagerUI::SetResourcePath(pwVar6);
    goto LAB_00408cfb;
  case 2:
    DuiLib::CDuiString::operator+=(local_98,L"res\\");
    pwVar6 = DuiLib::CDuiString::GetData(local_98);
    DuiLib::CPaintManagerUI::SetResourcePath(pwVar6);
    DuiLib::CPaintManagerUI::SetResourceZip(L"res.zip",true,(wchar_t *)0x0);
LAB_00408cfb:
    uVar9 = 0;
    pwVar6 = L"main.xml";
    pCVar5 = DuiLib::CResourceManager::GetInstance();
    DuiLib::CResourceManager::LoadResource(pCVar5,pwVar6,uVar9);
    break;
  case 3:
    DuiLib::CDuiString::operator+=(local_98,L"res\\");
    pwVar6 = DuiLib::CDuiString::GetData(local_98);
    DuiLib::CPaintManagerUI::SetResourcePath(pwVar6);
    puVar7 = &DAT_00427184;
    pwVar6 = L"IDR_RES";
    pCVar5 = DuiLib::CResourceManager::GetInstance();
    DuiLib::CResourceManager::LoadResource(pCVar5,pwVar6,puVar7);
    break;
  case 4:
    lpType = L"ZIPRES";
    pwVar6 = L"IDR_ZIPRES";
    pHVar2 = DuiLib::CPaintManagerUI::GetResourceDll();
    hResData = FindResourceW(pHVar2,pwVar6,lpType);
    if (hResData != (HRSRC)0x0) {
      pHVar8 = hResData;
      pHVar2 = DuiLib::CPaintManagerUI::GetResourceDll();
      hResData_00 = LoadResource(pHVar2,pHVar8);
      if (hResData_00 != (HGLOBAL)0x0) {
        pHVar8 = hResData;
        pHVar2 = DuiLib::CPaintManagerUI::GetResourceDll();
        DVar3 = SizeofResource(pHVar2,pHVar8);
        if (DVar3 != 0) {
          pwVar6 = L"LXD12345";
          pvVar4 = LockResource(hResData_00);
          DuiLib::CPaintManagerUI::SetResourceZip(pvVar4,DVar3,pwVar6);
          uVar9 = 0;
          pwVar6 = L"main.xml";
          pCVar5 = DuiLib::CResourceManager::GetInstance();
          DuiLib::CResourceManager::LoadResource(pCVar5,pwVar6,uVar9);
        }
      }
      FreeResource(hResData);
    }
  }
  DuiLib::CDuiString::~CDuiString(local_98);
  ExceptionList = local_10;
  return;
}


