#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE190_Integer_Overflow__char_fscanf_add_81.h"

namespace CWE190_Integer_Overflow__char_fscanf_add_81
{

void CWE190_Integer_Overflow__char_fscanf_add_81_bad::action(char data) const
{
    {
        char result = data + 1;
        printHexCharLine(result);
    }
}

}
#endif 
