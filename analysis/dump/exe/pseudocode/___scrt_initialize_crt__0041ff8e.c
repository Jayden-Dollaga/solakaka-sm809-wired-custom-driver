// Program: SM809 mouse Software.exe
// Function: ___scrt_initialize_crt
// Entry: 0041ff8e
// Body: 0041ff8e - 0041ffc6
// Signature: int ___scrt_initialize_crt(int param_1)


/* Library Function - Single Match
    ___scrt_initialize_crt
   
   Libraries: Visual Studio 2015 Release, Visual Studio 2017 Release, Visual Studio 2019 Release */

int __cdecl ___scrt_initialize_crt(int param_1)

{
  char cVar1;
  uint3 extraout_var;
  uint3 uVar2;
  undefined3 extraout_var_00;
  uint3 extraout_var_01;
  
  if (param_1 == 0) {
    DAT_00432720 = 1;
  }
  FUN_00420700();
  cVar1 = FUN_00420c0e();
  uVar2 = extraout_var;
  if (cVar1 != '\0') {
    cVar1 = FUN_00420c0e();
    if (cVar1 != '\0') {
      return CONCAT31(extraout_var_00,1);
    }
    FUN_00420c0e();
    uVar2 = extraout_var_01;
  }
  return (uint)uVar2 << 8;
}


