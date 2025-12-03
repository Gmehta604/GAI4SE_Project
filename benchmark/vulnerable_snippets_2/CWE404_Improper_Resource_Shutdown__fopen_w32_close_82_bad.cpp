#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE404_Improper_Resource_Shutdown__fopen_w32_close_82.h"

namespace CWE404_Improper_Resource_Shutdown__fopen_w32_close_82
{

void CWE404_Improper_Resource_Shutdown__fopen_w32_close_82_bad::action(FILE * data)
{
    if (data != NULL)
    {
        _close((int)data);
    }
}

}
#endif 
