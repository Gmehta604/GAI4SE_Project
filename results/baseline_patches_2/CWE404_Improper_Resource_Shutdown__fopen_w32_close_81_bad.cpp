#ifndef OMITBAD

#include <stdio.h>
#include <windows.h>

namespace CWE404_Improper_Resource_Shutdown__fopen_w32_close_81
{

void CWE404_Improper_Resource_Shutdown__fopen_w32_close_81_bad::action(FILE * data) const
{
    if (data != NULL)
    {
        fclose(data);
    }
}

}
#endif