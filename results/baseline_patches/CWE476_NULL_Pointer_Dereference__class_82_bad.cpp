#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE476_NULL_Pointer_Dereference__class_82.h"

namespace CWE476_NULL_Pointer_Dereference__class_82
{

void CWE476_NULL_Pointer_Dereference__class_82_bad::action(TwoIntsClass * data)
{
    if (data != NULL)
    {
        printIntLine(data->intOne);
        delete data;
    }
}

}
#endif