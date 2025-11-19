#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE843_Type_Confusion__char_81.h"

namespace CWE843_Type_Confusion__char_81
{

void CWE843_Type_Confusion__char_81_bad::action(void * data) const
{
    
    printIntLine(*((int*)data));
}

}
#endif