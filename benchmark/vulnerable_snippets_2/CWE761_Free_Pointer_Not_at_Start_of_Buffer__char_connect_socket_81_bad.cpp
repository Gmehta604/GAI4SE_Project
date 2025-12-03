#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE761_Free_Pointer_Not_at_Start_of_Buffer__char_connect_socket_81.h"

#define SEARCH_CHAR 'S'

namespace CWE761_Free_Pointer_Not_at_Start_of_Buffer__char_connect_socket_81
{

void CWE761_Free_Pointer_Not_at_Start_of_Buffer__char_connect_socket_81_bad::action(char * data) const
{
        for (; *data != '\0'; data++)
    {
        if (*data == SEARCH_CHAR)
        {
            printLine("We have a match!");
            break;
        }
    }
    free(data);
}

}
#endif 
