#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE761_Free_Pointer_Not_at_Start_of_Buffer__char_connect_socket_82.h"

#define SEARCH_CHAR 'S'

namespace CWE761_Free_Pointer_Not_at_Start_of_Buffer__char_connect_socket_82
{

void CWE761_Free_Pointer_Not_at_Start_of_Buffer__char_connect_socket_82_bad::action(char * data)
{
    size_t dataLen = strlen(data);
    char * dataCopy = (char *)malloc(dataLen+1);
    memcpy(dataCopy, data, dataLen);
    dataCopy[dataLen] = '\0';
    for (size_t i = 0; i < dataLen; i++)
    {
        if (dataCopy[i] == SEARCH_CHAR)
        {
            printLine("We have a match!");
            break;
        }
    }
    free(dataCopy);
}

}
#endif