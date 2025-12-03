#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE476_NULL_Pointer_Dereference__char_81.h"

namespace CWE476_NULL_Pointer_Dereference__char_81
{

void CWE476_NULL_Pointer_Dereference__char_81_bad::action(char * data) const
{

    printHexCharLine(data[0]);
}

}
#endif 
