#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE190_Integer_Overflow__char_fscanf_multiply_84.h"

namespace CWE190_Integer_Overflow__char_fscanf_multiply_84
{
CWE190_Integer_Overflow__char_fscanf_multiply_84_bad::CWE190_Integer_Overflow__char_fscanf_multiply_84_bad(char dataCopy)
{
    data = dataCopy;
    fscanf (stdin, "%c", &data);

    // Check for integer overflow before performing the multiplication
    if (data <= CHAR_MAX / 2)
    {
        char result = data * 2;
        printHexCharLine(result);
    }
    else
    {
        printLine("Input value is too large to perform arithmetic safely.");
    }
}

CWE190_Integer_Overflow__char_fscanf_multiply_84_bad::~CWE190_Integer_Overflow__char_fscanf_multiply_84_bad()
{
}
}
#endif