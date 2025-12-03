#ifndef OMITBAD

#include <climits>
#include <iostream>

namespace CWE190_Integer_Overflow__char_fscanf_add_82
{

void CWE190_Integer_Overflow__char_fscanf_add_82_bad::action(char data)
{
    if (data > CHAR_MAX - 1)
    {
        std::cout << "Possible overflow!" << std::endl;
    }
    else
    {
        char result = data + 1;
        printHexCharLine(result);
    }
}

}
#endif