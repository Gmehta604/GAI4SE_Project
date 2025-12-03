#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE194_Unexpected_Sign_Extension__connect_socket_malloc_81.h"

namespace CWE194_Unexpected_Sign_Extension__connect_socket_malloc_81
{

void CWE194_Unexpected_Sign_Extension__connect_socket_malloc_81_bad::action(short data) const
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