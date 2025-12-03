#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE761_Free_Pointer_Not_at_Start_of_Buffer__char_connect_socket_81.h"

#define SEARCH_CHAR 'S'

namespace CWE761_Free_Pointer_Not_at_Start_of_Buffer__char_connect_socket_81
{

void CWE761_Free_Pointer_Not_at_Start_of_Buffer__char_connect_socket_81_bad::action(char * data) const
{
    char * dataBadBuffer = (char *)malloc(50*sizeof(char));
    memset(dataBadBuffer, 'A', 50-1);
    dataBadBuffer[50-1] = '\0';
    /* FLAW: We are incrementing the pointer in the loop - this will cause us to free the
     * memory block without checking if it contains the search character */
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