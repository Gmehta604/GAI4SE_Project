#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE190_Integer_Overflow__char_fscanf_multiply_84.h"

namespace CWE190_Integer_Overflow__char_fscanf_multiply_84
{
CWE190_Integer_Overflow__char_fscanf_multiply_84_bad::CWE190_Integer_Overflow__char_fscanf_multiply_84_bad(char dataCopy)
{
    data = dataCopy;
    fscanf (stdin, "%c", &data);
}

CWE190_Integer_Overflow__char_fscanf_multiply_84_bad::~CWE190_Integer_Overflow__char_fscanf_multiply_84_bad()
{
    if(data > 0) 
    {
        char result = data * 2;
        printHexCharLine(result);
    }
}
}
#endif 
