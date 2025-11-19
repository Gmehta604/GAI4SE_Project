#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE190_Integer_Overflow__char_fscanf_add_84.h"

namespace CWE190_Integer_Overflow__char_fscanf_add_84
{
CWE190_Integer_Overflow__char_fscanf_add_84_bad::CWE190_Integer_Overflow__char_fscanf_add_84_bad(char dataCopy)
{
    data = dataCopy;
    fscanf (stdin, "%c", &data);
    if (data > CHAR_MAX - 1) {
        /* Handle overflow */
        printLine("Input value is too large to perform arithmetic safely.");
    } else {
        char result = data + 1;
        printHexCharLine(result);
    }
}

CWE190_Integer_Overflow__char_fscanf_add_84_bad::~CWE190_Integer_Overflow__char_fscanf_add_84_bad()
{
}
}
#endif