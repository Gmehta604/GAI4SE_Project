#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE476_NULL_Pointer_Dereference__int_82.h"

namespace CWE476_NULL_Pointer_Dereference__int_82
{

void CWE476_NULL_Pointer_Dereference__int_82_bad::action(int * data)
{
    printIntLine(*data);
}

}
#endif 
