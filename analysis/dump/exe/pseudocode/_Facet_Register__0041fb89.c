// Program: SM809 mouse Software.exe
// Function: _Facet_Register
// Entry: 0041fb89
// Body: 0041fb89 - 0041fbb4
// Signature: void _Facet_Register(_Facet_base * param_1)


/* Library Function - Single Match
    void __cdecl std::_Facet_Register(class std::_Facet_base *)
   
   Libraries: Visual Studio 2017 Release, Visual Studio 2019 Release */

void __cdecl std::_Facet_Register(_Facet_base *param_1)

{
  undefined4 *puVar1;
  
  puVar1 = operator_new(8);
  if (puVar1 == (undefined4 *)0x0) {
    puVar1 = (undefined4 *)0x0;
  }
  else {
    *puVar1 = DAT_00432710;
    puVar1[1] = param_1;
  }
  DAT_00432710 = puVar1;
  return;
}


