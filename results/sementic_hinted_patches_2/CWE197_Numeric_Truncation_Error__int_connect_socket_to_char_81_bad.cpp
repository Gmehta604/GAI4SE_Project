#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE197_Numeric_Truncation_Error__int_connect_socket_to_char_81.h"

namespace CWE197_Numeric_Truncation_Error__int_connect_socket_to_char_81
{

void CWE197_Numeric_Truncation_Error__int_connect_socket_to_char_81_bad::action(int data) const
{
    {
        char charData = (char)data;
        printHexCharLine(charData);
    }
}

}
#endif