#ifndef OMITBAD

#include <climits>
#include <iostream>

namespace CWE190_Integer_Overflow__char_fscanf_add_83
{
CWE190_Integer_Overflow__char_fscanf_add_83_bad::CWE190_Integer_Overflow__char_fscanf_add_83_bad(char dataCopy)
{
    data = dataCopy;
    fscanf (stdin, "%c", &data);

    // Check for overflows
    if (data > CHAR_MAX - 1)
    {
        std::cerr << "Error: Integer overflow detected." << std::endl;
        exit(EXIT_FAILURE);
    }
}

CWE190_Integer_Overflow__char_fscanf_add_83_bad::~CWE190_Integer_Overflow__char_fscanf_add_83_bad()
{
    {
        char result = data + 1;
        printHexCharLine(result);
    }
}
}
#endif