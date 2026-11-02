// Program: SM809 mouse Software.exe
// Function: FUN_00420540
// Entry: 00420540
// Body: 00420540 - 004206b2
// Signature: int FUN_00420540(void)


/* WARNING: Function: __SEH_prolog4 replaced with injection: SEH_prolog4 */

int FUN_00420540(void)

{
  code *pcVar1;
  bool bVar2;
  int iVar3;
  undefined4 uVar4;
  int *piVar5;
  char *pcVar6;
  uint uVar7;
  int unaff_ESI;
  undefined4 uVar8;
  undefined4 uVar9;
  void *local_14;
  
  iVar3 = ___scrt_initialize_crt(1);
  if ((char)iVar3 != '\0') {
    bVar2 = false;
    uVar4 = ___scrt_acquire_startup_lock();
    if (DAT_00432718 != 1) {
      if (DAT_00432718 == 0) {
        DAT_00432718 = 1;
        iVar3 = initterm_e(&DAT_00424650,&DAT_0042465c);
        if (iVar3 != 0) {
          ExceptionList = local_14;
          return 0xff;
        }
        initterm(&DAT_0042461c,&DAT_0042464c);
        DAT_00432718 = 2;
      }
      else {
        bVar2 = true;
      }
      ___scrt_release_startup_lock((char)uVar4);
      piVar5 = (int *)FUN_00420c61();
      if ((*piVar5 != 0) &&
         (uVar4 = ___scrt_is_nonwritable_in_current_image((int)piVar5), (char)uVar4 != '\0')) {
        pcVar1 = (code *)*piVar5;
        uVar9 = 0;
        uVar8 = 2;
        uVar4 = 0;
        guard_check_icall();
        (*pcVar1)(uVar4,uVar8,uVar9);
      }
      piVar5 = (int *)FUN_00420c67();
      if ((*piVar5 != 0) &&
         (uVar4 = ___scrt_is_nonwritable_in_current_image((int)piVar5), (char)uVar4 != '\0')) {
        register_thread_local_exe_atexit_callback(*piVar5);
      }
      ___scrt_get_show_window_mode();
      pcVar6 = (char *)get_narrow_winmain_command_line();
      unaff_ESI = FUN_00408e50((HINSTANCE__ *)&IMAGE_DOS_HEADER_00400000,0,pcVar6);
      uVar7 = FUN_00420a35();
      if ((char)uVar7 != '\0') {
        if (!bVar2) {
          _cexit();
        }
        ___scrt_uninitialize_crt(1,'\0');
        ExceptionList = local_14;
        return unaff_ESI;
      }
      goto LAB_004206ad;
    }
  }
  FUN_004208e1();
LAB_004206ad:
                    /* WARNING: Subroutine does not return */
  exit(unaff_ESI);
}


