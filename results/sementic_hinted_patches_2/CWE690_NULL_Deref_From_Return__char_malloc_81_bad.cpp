#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE690_NULL_Deref_From_Return__char_malloc_81.h"

namespace CWE690_NULL_Deref_From_Return__char_malloc_81
{

void CWE690_NULL_Deref_From_Return__char_malloc_81_bad::action(char * data) const
{
    if (data == NULL) {
        data = malloc(100*sizeof(char));
        if (data == NULL) {
            return;
        }
    }
    strcpy(data, "Initialize");
    printLine(data);
    free(data);
}

}
#endif