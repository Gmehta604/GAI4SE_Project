#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE476_NULL_Pointer_Dereference__int64_t_82.h"

namespace CWE476_NULL_Pointer_Dereference__int64_t_82
{

void CWE476_NULL_Pointer_Dereference__int64_t_82_bad::action(int64_t * data)
{
    if (data != NULL)
    {
        printLongLongLine(*data);
    }
}

}
#endif