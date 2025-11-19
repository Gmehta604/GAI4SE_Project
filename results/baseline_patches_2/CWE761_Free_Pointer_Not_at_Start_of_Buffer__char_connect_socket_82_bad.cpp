#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE761_Free_Pointer_Not_at_Start_of_Buffer__char_connect_socket_82.h"

#define SEARCH_CHAR 'S'

namespace CWE761_Free_Pointer_Not_at_Start_of_Buffer__char_connect_socket_82
{

void CWE761_Free_Pointer_Not_at_Start_of_Buffer__char_connect_socket_82_bad::action(char * data)
{
    char * dataBadBuffer = (char *)malloc(50*sizeof(char));
    memset(dataBadBuffer, 'A', 50-1);
    dataBadBuffer[50-1] = '\0';
    /* FLAW: We are incrementing the pointer in the loop - this will cause us to free the
     * memory block not at the start of the buffer */
    for (; *data != '\0'; data++)
    {
        if (*data == SEARCH_CHAR)
        {
            printLine("We have a match!");
            break;
        }
    }
    free(dataBadBuffer);
}

}
#endif