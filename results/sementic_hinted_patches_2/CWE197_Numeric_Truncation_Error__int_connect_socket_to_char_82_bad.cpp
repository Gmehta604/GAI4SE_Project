#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE197_Numeric_Truncation_Error__int_connect_socket_to_char_82.h"

namespace CWE197_Numeric_Truncation_Error__int_connect_socket_to_char_82
{

void CWE197_Numeric_Truncation_Error__int_connect_socket_to_char_82_bad::action(int data)
{
    {
        char charData = (char)data;
        printHexCharLine(charData);
    }
}

}
#endif