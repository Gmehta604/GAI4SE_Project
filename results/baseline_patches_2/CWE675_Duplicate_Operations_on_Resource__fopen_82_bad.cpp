#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE675_Duplicate_Operations_on_Resource__fopen_82.h"

namespace CWE675_Duplicate_Operations_on_Resource__fopen_82
{

void CWE675_Duplicate_Operations_on_Resource__fopen_82_bad::action(FILE * data)
{
    
    if (data != NULL)
    {
        fclose(data);
    }
}

}
#endif