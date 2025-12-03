#ifndef OMITBAD

#include <iostream>
#include <limits>

namespace CWE190_Integer_Overflow__char_fscanf_multiply_84
{
CWE190_Integer_Overflow__char_fscanf_multiply_84_bad::CWE190_Integer_Overflow__char_fscanf_multiply_84_bad(char dataCopy)
{
    data = dataCopy;
    fscanf (stdin, "%c", &data);

    // Check for overflows
    if (data > std::numeric_limits<char>::max() / 2)
    {
        // Handle overflow
        std::cout << "Input value is too large to perform arithmetic safely." << std::endl;
    }
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