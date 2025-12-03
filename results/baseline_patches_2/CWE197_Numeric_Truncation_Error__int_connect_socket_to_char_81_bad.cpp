#ifndef OMITBAD

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <arpa/inet.h>

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