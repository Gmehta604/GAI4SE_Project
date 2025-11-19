#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE126_Buffer_Overread__char_alloca_loop_82.h"

namespace CWE126_Buffer_Overread__char_alloca_loop_82
{

void CWE126_Buffer_Overread__char_alloca_loop_82_bad::action(char * data)
{
    {
        size_t i, destLen;
        char dest[100];
        memset(dest, 'C', 99);
        dest[99] = '\0'; 
        destLen = strlen(dest);
        for (i = 0; i < destLen; i++)
        {
            dest[i] = data[i];
        }
        dest[99] = '\0';
        printLine(dest);
    }
}

}
#endif