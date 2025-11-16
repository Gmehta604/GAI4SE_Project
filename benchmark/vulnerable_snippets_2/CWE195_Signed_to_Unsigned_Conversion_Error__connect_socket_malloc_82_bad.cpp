
#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE195_Signed_to_Unsigned_Conversion_Error__connect_socket_malloc_82.h"

namespace CWE195_Signed_to_Unsigned_Conversion_Error__connect_socket_malloc_82
{

void CWE195_Signed_to_Unsigned_Conversion_Error__connect_socket_malloc_82_bad::action(int data)
{

    if (data < 100)
    {
        char * dataBuffer = (char *)malloc(data);
        if (dataBuffer == NULL) {exit(-1);}
        memset(dataBuffer, 'A', data-1);
        dataBuffer[data-1] = '\0';
        printLine(dataBuffer);
        free(dataBuffer);
    }
}

}
#endif 
