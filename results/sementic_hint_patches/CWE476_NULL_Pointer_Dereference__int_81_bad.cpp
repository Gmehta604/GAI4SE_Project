#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE476_NULL_Pointer_Dereference__int_81.h"

namespace CWE476_NULL_Pointer_Dereference__int_81
{

void CWE476_NULL_Pointer_Dereference__int_81_bad::action(int * data) const
{
    if (data != NULL)
    {
        printIntLine(*data);
    }
}

}
#endif