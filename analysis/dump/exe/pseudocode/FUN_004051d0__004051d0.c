// Program: SM809 mouse Software.exe
// Function: FUN_004051d0
// Entry: 004051d0
// Body: 004051d0 - 0040524e
// Signature: basic_streambuf<char,std::char_traits<char>_> * FUN_004051d0(basic_streambuf<char,std::char_traits<char>_> * param_1)


basic_streambuf<char,std::char_traits<char>_> * __fastcall
FUN_004051d0(basic_streambuf<char,std::char_traits<char>_> *param_1)

{
  int iVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  bool bVar4;
  int iVar5;
  basic_streambuf<char,std::char_traits<char>_> *pbVar6;
  
  if (*(int *)(param_1 + 0x4c) != 0) {
    if ((basic_streambuf<char,std::char_traits<char>_> *)**(int **)(param_1 + 0xc) == param_1 + 0x3c
       ) {
      iVar5 = *(int *)(param_1 + 0x54);
      iVar1 = *(int *)(param_1 + 0x50);
      **(int **)(param_1 + 0xc) = iVar1;
      **(int **)(param_1 + 0x1c) = iVar1;
      **(int **)(param_1 + 0x2c) = iVar5 - iVar1;
    }
    bVar4 = FUN_00405100((int *)param_1);
    pbVar6 = param_1;
    if (!bVar4) {
      pbVar6 = (basic_streambuf<char,std::char_traits<char>_> *)0x0;
    }
    iVar5 = fclose(*(FILE **)(param_1 + 0x4c));
    if (iVar5 == 0) goto LAB_0040521a;
  }
  pbVar6 = (basic_streambuf<char,std::char_traits<char>_> *)0x0;
LAB_0040521a:
  param_1[0x48] = (basic_streambuf<char,std::char_traits<char>_>)0x0;
  param_1[0x3d] = (basic_streambuf<char,std::char_traits<char>_>)0x0;
  std::basic_streambuf<char,std::char_traits<char>_>::_Init(param_1);
  uVar3 = DAT_00432a88;
  uVar2 = DAT_00432a84;
  *(undefined4 *)(param_1 + 0x4c) = 0;
  *(undefined4 *)(param_1 + 0x40) = uVar2;
  *(undefined4 *)(param_1 + 0x44) = uVar3;
  *(undefined4 *)(param_1 + 0x38) = 0;
  return pbVar6;
}


