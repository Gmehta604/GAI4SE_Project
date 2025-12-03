#ifndef OMITBAD

#include <climits>
#include <iostream>

namespace CWE190_Integer_Overflow__char_fscanf_multiply_83
{
CWE190_Integer_Overflow__char_fscanf_multiply_83_bad::CWE190_Integer_Overflow__char_fscanf_multiply_83_bad(char dataCopy)
{
    data = dataCopy;
    fscanf (stdin, "%c", &data);

    // Check for overflows
    if(data > CHAR_MAX/2)
    {
        std::cout << "Value too large to perform arithmetic safely." << std::endl;
    }
    else
    {
        char result = data * 2;
        printHexCharLine(result);
    }
}

CWE190_Integer_Overflow__char_fscanf_multiply_83_bad::~CWE190_Integer_Overflow__char_fscanf_multiply_83_bad()
{
}
}
#endif