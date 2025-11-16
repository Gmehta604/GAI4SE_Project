#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE404_Improper_Resource_Shutdown__fopen_w32_close_81.h"

namespace CWE404_Improper_Resource_Shutdown__fopen_w32_close_81
{

void CWE404_Improper_Resource_Shutdown__fopen_w32_close_81_bad::action(FILE * data) const
{
    if (data != NULL)
    {
        _close((int)data);
    }
}

}
#endif 
