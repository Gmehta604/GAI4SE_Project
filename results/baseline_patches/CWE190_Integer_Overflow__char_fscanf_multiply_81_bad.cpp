#ifndef OMITBAD

#include <climits>
#include <iostream>

namespace CWE190_Integer_Overflow__char_fscanf_multiply_81
{

void CWE190_Integer_Overflow__char_fscanf_multiply_81_bad::action(char data) const
{
    if (data > CHAR_MAX / 2)
    {
        std::cout << "data is greater than CHAR_MAX / 2" << std::endl;
    }
    else
    {
        char result = data * 2;
        printHexCharLine(result);
    }
}

}
#endif