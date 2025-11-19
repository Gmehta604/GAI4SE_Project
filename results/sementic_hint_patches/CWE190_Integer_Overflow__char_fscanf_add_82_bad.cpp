#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE190_Integer_Overflow__char_fscanf_add_82.h"

namespace CWE190_Integer_Overflow__char_fscanf_add_82
{

void CWE190_Integer_Overflow__char_fscanf_add_82_bad::action(char data)
{
    if (data < CHAR_MAX)
    {
        char result = data + 1;
        printHexCharLine(result);
    }
    else
    {
        // Handle the case where data is at its maximum value
        // ...
    }
}

}
#endif