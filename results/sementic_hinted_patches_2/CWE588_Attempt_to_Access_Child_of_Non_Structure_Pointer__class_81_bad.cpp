#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE588_Attempt_to_Access_Child_of_Non_Structure_Pointer__class_81.h"

namespace CWE588_Attempt_to_Access_Child_of_Non_Structure_Pointer__class_81
{

void CWE588_Attempt_to_Access_Child_of_Non_Structure_Pointer__class_81_bad::action(void * data) const
{

    TwoIntsClass* classPtr = reinterpret_cast<TwoIntsClass*>(data);
    printIntLine(classPtr->intTwo);
}

}
#endif