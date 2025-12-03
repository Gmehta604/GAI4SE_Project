
#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE127_Buffer_Underread__char_alloca_cpy_81.h"

namespace CWE127_Buffer_Underread__char_alloca_cpy_81
{

void CWE127_Buffer_Underread__char_alloca_cpy_81_bad::action(char * data) const
{
    {
        char dest[100*2];
        memset(dest, 'C', 100*2-1); 
        dest[100*2-1] = '\0'; 
        strcpy(dest, data);
        printLine(dest);
    }
}

}
#endif 
