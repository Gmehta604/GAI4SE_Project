#ifndef OMITBAD

#include <climits>
#include <iostream>

namespace CWE190_Integer_Overflow__char_fscanf_add_84
{
CWE190_Integer_Overflow__char_fscanf_add_84_bad::CWE190_Integer_Overflow__char_fscanf_add_84_bad(char dataCopy)
{
    data = dataCopy;
    fscanf (stdin, "%hhd", &data);
}

CWE190_Integer_Overflow__char_fscanf_add_84_bad::~CWE190_Integer_Overflow__char_fscanf_add_84_bad()
{
    {
        char result = data + 1;
        if (result > CHAR_MAX)
        {
            std::cout << "result is greater than CHAR_MAX" << std::endl;
        }
        else
        {
            printHexCharLine(result);
        }
    }
}
}
#endif