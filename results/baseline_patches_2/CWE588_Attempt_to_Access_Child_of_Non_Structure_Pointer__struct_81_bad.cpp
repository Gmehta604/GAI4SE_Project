#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE588_Attempt_to_Access_Child_of_Non_Structure_Pointer__struct_81.h"

namespace CWE588_Attempt_to_Access_Child_of_Non_Structure_Pointer__struct_81
{

void CWE588_Attempt_to_Access_Child_of_Non_Structure_Pointer__struct_81_bad::action(void * data) const
{
    
    if (data != NULL && !isBadPointer(data))
    {
        printStructLine((twoIntsStruct *)data);
    }
    else
    {
        printLine("ERROR: Array index is negative.");
    }
}

}
#endif