
#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE191_Integer_Underflow__char_fscanf_multiply_81.h"

namespace CWE191_Integer_Underflow__char_fscanf_multiply_81
{

void CWE191_Integer_Underflow__char_fscanf_multiply_81_bad::action(char data) const
{
    if(data < 0) 
    {
        char result = data * 2;
        printHexCharLine(result);
    }
}

}
#endif 
