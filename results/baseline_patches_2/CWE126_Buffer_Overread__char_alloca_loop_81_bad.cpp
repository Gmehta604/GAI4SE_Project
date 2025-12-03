#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE126_Buffer_Overread__char_alloca_loop_81.h"

namespace CWE126_Buffer_Overread__char_alloca_loop_81
{

void CWE126_Buffer_Overread__char_alloca_loop_81_bad::action(char * data) const
{
    {
        size_t i;
        char dest[100];
        memset(dest, 'C', 99);
        dest[99] = '\0';
        for (i = 0; i < 99; i++)
        {
            dest[i] = data[i];
        }
        dest[99] = '\0';
        printLine(dest);
    }
}

}
#endif