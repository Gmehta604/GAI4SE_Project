
#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE126_Buffer_Overread__char_alloca_loop_81.h"

namespace CWE126_Buffer_Overread__char_alloca_loop_81
{

void CWE126_Buffer_Overread__char_alloca_loop_81_bad::action(char * data) const
{
    {
        size_t i, destLen;
        char dest[100];
        memset(dest, 'C', 100-1);
        dest[100-1] = '\0';
        destLen = strlen(dest);
        for (i = 0; i < destLen; i++)
        {
            dest[i] = data[i];
        }
        dest[100-1] = '\0';
        printLine(dest);
    }
}

}
#endif 
