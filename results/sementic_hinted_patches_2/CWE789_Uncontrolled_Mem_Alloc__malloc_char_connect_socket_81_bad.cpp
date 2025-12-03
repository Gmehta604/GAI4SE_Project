#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE789_Uncontrolled_Mem_Alloc__malloc_char_connect_socket_81.h"

#define HELLO_STRING "hello"

namespace CWE789_Uncontrolled_Mem_Alloc__malloc_char_connect_socket_81
{

void CWE789_Uncontrolled_Mem_Alloc__malloc_char_connect_socket_81_bad::action(size_t data) const
{
    {
        char * myString;
                
        if (data > strlen(HELLO_STRING))
        {
            myString = (char *)malloc(data*sizeof(char));
            if (myString == NULL) {exit(-1);}
            
            strncpy(myString, HELLO_STRING, data-1);
            myString[data-1] = '\0';
            printLine(myString);
            free(myString);
        }
        else
        {
            printLine("Input is less than the length of the source string");
        }
    }
}

}
#endif