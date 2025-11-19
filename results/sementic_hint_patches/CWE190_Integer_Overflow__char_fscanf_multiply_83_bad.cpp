#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE190_Integer_Overflow__char_fscanf_multiply_83.h"

namespace CWE190_Integer_Overflow__char_fscanf_multiply_83
{
CWE190_Integer_Overflow__char_fscanf_multiply_83_bad::CWE190_Integer_Overflow__char_fscanf_multiply_83_bad(char dataCopy)
{
    data = dataCopy;
    fscanf (stdin, "%c", &data);
}

CWE190_Integer_Overflow__char_fscanf_multiply_83_bad::~CWE190_Integer_Overflow__char_fscanf_multiply_83_bad()
{
    if(data > 0 && data <= CHAR_MAX / 2) 
    {
        char result = data * 2;
        printHexCharLine(result);
    }
}
}
#endif