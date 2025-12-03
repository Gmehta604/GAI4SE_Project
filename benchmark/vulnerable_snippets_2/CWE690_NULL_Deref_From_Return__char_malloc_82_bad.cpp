#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE690_NULL_Deref_From_Return__char_malloc_82.h"

namespace CWE690_NULL_Deref_From_Return__char_malloc_82
{

void CWE690_NULL_Deref_From_Return__char_malloc_82_bad::action(char * data)
{
    
    strcpy(data, "Initialize");
    printLine(data);
    free(data);
}

}
#endif 
