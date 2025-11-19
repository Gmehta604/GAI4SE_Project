#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE195_Signed_to_Unsigned_Conversion_Error__connect_socket_malloc_81.h"

namespace CWE195_Signed_to_Unsigned_Conversion_Error__connect_socket_malloc_81
{

void CWE195_Signed_to_Unsigned_Conversion_Error__connect_socket_malloc_81_bad::action(int data) const
{
    
    if (data < 100)
    {
        char * dataBuffer = (char *)malloc(data);
        if (dataBuffer == NULL) {exit(-1);}
        
        memset(dataBuffer, 'A', data);
        dataBuffer[data] = '\0';
        printLine(dataBuffer);
        free(dataBuffer);
    }
}

}
#endif