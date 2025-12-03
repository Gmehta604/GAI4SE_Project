#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE476_NULL_Pointer_Dereference__class_81.h"

namespace CWE476_NULL_Pointer_Dereference__class_81
{

void CWE476_NULL_Pointer_Dereference__class_81_bad::action(TwoIntsClass * data) const
{
    if (data != nullptr)
    {
        printIntLine(data->intOne);
        delete data;
    }
}

}
#endif