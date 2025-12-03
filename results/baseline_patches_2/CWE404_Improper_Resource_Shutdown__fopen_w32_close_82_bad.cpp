#ifndef OMITBAD

#include <stdio.h>
#include <windows.h>

namespace CWE404_Improper_Resource_Shutdown__fopen_w32_close_82
{

void CWE404_Improper_Resource_Shutdown__fopen_w32_close_82_bad::action(FILE * data)
{
    if (data != NULL)
    {
        fclose(data);
    }
}

}
#endif