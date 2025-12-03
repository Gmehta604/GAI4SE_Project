#ifndef OMITBAD

#include <stdio.h>

namespace CWE675_Duplicate_Operations_on_Resource__fopen_81
{

void CWE675_Duplicate_Operations_on_Resource__fopen_81_bad::action(FILE * data) const
{
    
    if (data != NULL)
    {
        fclose(data);
    }
}

}
#endif