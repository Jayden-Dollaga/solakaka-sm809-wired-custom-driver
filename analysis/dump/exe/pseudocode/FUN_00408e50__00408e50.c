// Program: SM809 mouse Software.exe
// Function: FUN_00408e50
// Entry: 00408e50
// Body: 00408e50 - 00409019
// Signature: undefined4 FUN_00408e50(HINSTANCE__ * param_1, undefined4 param_2, char * param_3)


/* WARNING: Function: __security_check_cookie replaced with injection: security_check_cookie */

undefined4 FUN_00408e50(HINSTANCE__ *param_1,undefined4 param_2,char *param_3)

{
  char cVar1;
  HANDLE hObject;
  DWORD DVar2;
  HWND hWnd;
  wchar_t *lpOutputString;
  HRESULT HVar3;
  WindowImplBase *pWVar4;
  CDuiString *this;
  char *pcVar5;
  CDuiString local_190 [132];
  char local_10c [260];
  undefined4 local_8;
  
  local_8 = DAT_00432008 ^ (uint)(local_10c + 0x108);
  hObject = CreateMutexW((LPSECURITY_ATTRIBUTES)0x0,0,L"Mosue Driver Configure Jack Ma");
  DVar2 = GetLastError();
  if (DVar2 == 0xb7) {
    hWnd = FindWindowW(L"Mouse Driver",(LPCWSTR)0x0);
    if (hWnd != (HWND)0x0) {
      SendMessageW(hWnd,0x40d,0,0);
    }
    CloseHandle(hObject);
    return 1;
  }
  memset(local_10c,0,0x104);
  strcpy_s(local_10c,0x104,param_3);
  pcVar5 = local_10c;
  do {
    cVar1 = *pcVar5;
    pcVar5 = pcVar5 + 1;
  } while (cVar1 != '\0');
  DuiLib::CDuiString::CDuiString(local_190);
  DuiLib::CDuiString::Format
            (this,(wchar_t *)local_190,L"ilen = %d\r\n",(int)pcVar5 - (int)(local_10c + 1));
  lpOutputString = DuiLib::CDuiString::operator_wchar_t_const_(local_190);
  OutputDebugStringW(lpOutputString);
  HVar3 = CoInitialize((LPVOID)0x0);
  if (-1 < HVar3) {
    OleInitialize((LPVOID)0x0);
    DuiLib::CPaintManagerUI::SetInstance(param_1);
    FUN_00408c70();
    pWVar4 = operator_new(0x1af8);
    memset(pWVar4,0,0x1af8);
    pWVar4 = FUN_00414980(pWVar4);
    if (pWVar4 != (WindowImplBase *)0x0) {
      DuiLib::CWindowWnd::Create
                ((CWindowWnd *)pWVar4,(HWND__ *)0x0,(wchar_t *)0x0,0x96c80000,0,0,0,800,0x23c,
                 (HMENU__ *)0x0);
      DuiLib::CWindowWnd::CenterWindow((CWindowWnd *)pWVar4);
      if (((DAT_00432aa4 == 0) || (0 < (int)pcVar5 - (int)(local_10c + 1))) ||
         (*(int *)(pWVar4 + 0x16d0) == 0)) {
        DuiLib::CWindowWnd::ShowWindow((CWindowWnd *)pWVar4,false,true);
      }
      DuiLib::CPaintManagerUI::MessageLoop();
      (**(code **)(*(int *)pWVar4 + 0x14))(1);
      DuiLib::CPaintManagerUI::Term();
      OleUninitialize();
      CoUninitialize();
    }
  }
  DuiLib::CDuiString::~CDuiString(local_190);
  return 0;
}


