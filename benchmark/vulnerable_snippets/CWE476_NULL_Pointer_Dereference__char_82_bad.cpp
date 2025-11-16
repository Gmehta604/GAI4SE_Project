#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE476_NULL_Pointer_Dereference__char_82.h"

namespace CWE476_NULL_Pointer_Dereference__char_82
{

void CWE476_NULL_Pointer_Dereference__char_82_bad::action(char * data)
{

    printHexCharLine(data[0]);
}

}
#endif 
