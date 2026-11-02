// Program: SM809 mouse Software.exe
// Function: Insert_node
// Entry: 00405e10
// Body: 00405e10 - 00406014
// Signature: int * Insert_node(void * this, int * param_1, int param_2, int * param_3)


/* Library Function - Multiple Matches With Same Base Name
    public: struct std::_Tree_node<unsigned int,void *> * __thiscall std::_Tree_val<struct
   std::_Tree_simple_types<unsigned int> >::_Insert_node(struct std::_Tree_id<struct
   std::_Tree_node<unsigned int,void *> *>,struct std::_Tree_node<unsigned int,void *> * const)
    public: struct std::_Tree_node<struct fuzzer::TracePC::PCTableEntry const *,void *> * __thiscall
   std::_Tree_val<struct std::_Tree_simple_types<struct fuzzer::TracePC::PCTableEntry const *>
   >::_Insert_node(struct std::_Tree_id<struct std::_Tree_node<struct fuzzer::TracePC::PCTableEntry
   const *,void *> *>,struct std::_Tree_node<struct fuzzer::TracePC::PCTableEntry const *,void *> *
   const)
    public: struct std::_Tree_node<class std::basic_string<char,struct std::char_traits<char>,class
   std::allocator<char> >,void *> * __thiscall std::_Tree_val<struct std::_Tree_simple_types<class
   std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > >
   >::_Insert_node(struct std::_Tree_id<struct std::_Tree_node<class std::basic_string<char,struct
   std::char_traits<char>,class std::allocator<char> >,void *> *>,struct std::_Tree_node<class
   std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,void *> *
   const)
   
   Library: Visual Studio 2019 Release */

int * __thiscall Insert_node(void *this,int *param_1,int param_2,int *param_3)

{
  char cVar1;
  int *piVar2;
  int *piVar3;
  undefined4 *puVar4;
  int iVar5;
  int *piVar6;
  int *piVar7;
  int *piVar8;
  int *piVar9;
  int *piVar10;
  
  piVar2 = *(int **)this;
  *(int *)((int)this + 4) = *(int *)((int)this + 4) + 1;
  param_3[1] = (int)param_1;
  if (param_1 == piVar2) {
    *piVar2 = (int)param_3;
    piVar2[1] = (int)param_3;
    piVar2[2] = (int)param_3;
    *(undefined1 *)(param_3 + 3) = 1;
    return param_3;
  }
  if (param_2 == 0) {
    param_1[2] = (int)param_3;
    if (param_1 == (int *)piVar2[2]) {
      piVar2[2] = (int)param_3;
    }
  }
  else {
    *param_1 = (int)param_3;
    if (param_1 == (int *)*piVar2) {
      *piVar2 = (int)param_3;
    }
  }
  cVar1 = *(char *)(param_3[1] + 0xc);
  piVar8 = param_3;
  do {
    if (cVar1 != '\0') {
      *(undefined1 *)(piVar2[1] + 0xc) = 1;
      return param_3;
    }
    piVar9 = (int *)piVar8[1];
    piVar7 = piVar8 + 1;
    piVar10 = piVar9 + 1;
    iVar5 = *(int *)piVar9[1];
    if (piVar9 == (int *)iVar5) {
      iVar5 = ((int *)piVar9[1])[2];
      if (*(char *)(iVar5 + 0xc) == '\0') goto LAB_00405f46;
      piVar3 = (int *)piVar9[2];
      if (piVar8 == piVar3) {
        piVar9[2] = *piVar3;
        if (*(char *)(*piVar3 + 0xd) == '\0') {
          *(int **)(*piVar3 + 4) = piVar9;
        }
        piVar3[1] = *piVar10;
        if (piVar9 == (int *)*(int *)(*(int *)this + 4)) {
          *(int **)(*(int *)this + 4) = piVar3;
          *piVar3 = (int)piVar9;
          *piVar10 = (int)piVar3;
          piVar8 = piVar9;
          piVar9 = piVar3;
          piVar7 = piVar10;
        }
        else {
          piVar8 = (int *)*piVar10;
          if (piVar9 == (int *)*piVar8) {
            *piVar8 = (int)piVar3;
            *piVar3 = (int)piVar9;
            *piVar10 = (int)piVar3;
            piVar8 = piVar9;
            piVar9 = piVar3;
            piVar7 = piVar10;
          }
          else {
            piVar8[2] = (int)piVar3;
            *piVar3 = (int)piVar9;
            *piVar10 = (int)piVar3;
            piVar8 = piVar9;
            piVar9 = piVar3;
            piVar7 = piVar10;
          }
        }
      }
      *(undefined1 *)(piVar9 + 3) = 1;
      *(undefined1 *)(*(int *)(*piVar7 + 4) + 0xc) = 0;
      piVar7 = *(int **)(*piVar7 + 4);
      piVar10 = (int *)*piVar7;
      *piVar7 = piVar10[2];
      if (*(char *)(piVar10[2] + 0xd) == '\0') {
        *(int **)(piVar10[2] + 4) = piVar7;
      }
      piVar10[1] = piVar7[1];
      if (piVar7 == *(int **)(*(int *)this + 4)) {
        *(int **)(*(int *)this + 4) = piVar10;
        piVar10[2] = (int)piVar7;
      }
      else {
        piVar9 = (int *)piVar7[1];
        if (piVar7 == (int *)piVar9[2]) {
          piVar9[2] = (int)piVar10;
          piVar10[2] = (int)piVar7;
        }
        else {
          *piVar9 = (int)piVar10;
          piVar10[2] = (int)piVar7;
        }
      }
LAB_00405fef:
      piVar7[1] = (int)piVar10;
    }
    else {
      if (*(char *)(iVar5 + 0xc) != '\0') {
        piVar3 = (int *)*piVar9;
        piVar6 = piVar9;
        if (piVar8 == piVar3) {
          *piVar9 = piVar3[2];
          if (*(char *)(piVar3[2] + 0xd) == '\0') {
            *(int **)(piVar3[2] + 4) = piVar9;
          }
          piVar3[1] = *piVar10;
          if (piVar9 == *(int **)(*(int *)this + 4)) {
            *(int **)(*(int *)this + 4) = piVar3;
          }
          else {
            puVar4 = (undefined4 *)*piVar10;
            if (piVar9 == (int *)puVar4[2]) {
              puVar4[2] = piVar3;
            }
            else {
              *puVar4 = piVar3;
            }
          }
          piVar3[2] = (int)piVar9;
          *piVar10 = (int)piVar3;
          piVar6 = piVar3;
          piVar8 = piVar9;
          piVar7 = piVar10;
        }
        *(undefined1 *)(piVar6 + 3) = 1;
        *(undefined1 *)(*(int *)(*piVar7 + 4) + 0xc) = 0;
        piVar7 = *(int **)(*piVar7 + 4);
        piVar10 = (int *)piVar7[2];
        piVar7[2] = *piVar10;
        if (*(char *)(*piVar10 + 0xd) == '\0') {
          *(int **)(*piVar10 + 4) = piVar7;
        }
        piVar10[1] = piVar7[1];
        if (piVar7 == *(int **)(*(int *)this + 4)) {
          *(int **)(*(int *)this + 4) = piVar10;
        }
        else {
          piVar9 = (int *)piVar7[1];
          if (piVar7 == (int *)*piVar9) {
            *piVar9 = (int)piVar10;
          }
          else {
            piVar9[2] = (int)piVar10;
          }
        }
        *piVar10 = (int)piVar7;
        goto LAB_00405fef;
      }
LAB_00405f46:
      *(undefined1 *)(piVar9 + 3) = 1;
      *(undefined1 *)(iVar5 + 0xc) = 1;
      *(undefined1 *)(*(int *)(*piVar7 + 4) + 0xc) = 0;
      piVar8 = *(int **)(*piVar7 + 4);
    }
    cVar1 = *(char *)(piVar8[1] + 0xc);
  } while( true );
}


