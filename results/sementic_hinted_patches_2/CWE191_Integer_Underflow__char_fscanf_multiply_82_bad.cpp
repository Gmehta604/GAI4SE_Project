#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE191_Integer_Underflow__char_fscanf_multiply_82.h"

namespace CWE191_Integer_Underflow__char_fscanf_multiply_82
{

void CWE191_Integer_Underflow__char_fscanf_multiply_82_bad::action(char data)
{
    if(data >= 0) 
    {
        char result = data * 2;
        printHexCharLine(result);
    }
}

}
#endif