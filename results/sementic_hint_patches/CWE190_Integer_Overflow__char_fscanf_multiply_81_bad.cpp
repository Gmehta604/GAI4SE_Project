#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE190_Integer_Overflow__char_fscanf_multiply_81.h"

namespace CWE190_Integer_Overflow__char_fscanf_multiply_81
{

void CWE190_Integer_Overflow__char_fscanf_multiply_81_bad::action(char data) const
{
    if(data > 0 && data <= CHAR_MAX/2) 
    {
        char result = data * 2;
        printHexCharLine(result);
    }
}

}
#endif