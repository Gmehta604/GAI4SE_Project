
#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE194_Unexpected_Sign_Extension__connect_socket_malloc_82.h"

namespace CWE194_Unexpected_Sign_Extension__connect_socket_malloc_82
{

void CWE194_Unexpected_Sign_Extension__connect_socket_malloc_82_bad::action(short data)
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
