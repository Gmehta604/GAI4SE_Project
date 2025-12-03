#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE190_Integer_Overflow__char_fscanf_add_81.h"

namespace CWE190_Integer_Overflow__char_fscanf_add_81
{

void CWE190_Integer_Overflow__char_fscanf_add_81_bad::action(char data) const
{
    if (data < CHAR_MAX)
    {
        char result = data + 1;
        printHexCharLine(result);
    }
    else
    {
        // Handle the case where data == CHAR_MAX
        // Preventing the overflow
    }
}

}
#endif