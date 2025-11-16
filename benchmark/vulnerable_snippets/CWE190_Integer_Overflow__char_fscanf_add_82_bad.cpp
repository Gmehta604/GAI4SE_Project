#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE190_Integer_Overflow__char_fscanf_add_82.h"

namespace CWE190_Integer_Overflow__char_fscanf_add_82
{

void CWE190_Integer_Overflow__char_fscanf_add_82_bad::action(char data)
{
    {
        char result = data + 1;
        printHexCharLine(result);
    }
}

}
#endif 
