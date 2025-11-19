#ifndef OMITBAD

#include <stdlib.h>
#include <string.h>

void CWE690_NULL_Deref_From_Return__char_malloc_82_bad::action(char * data)
{
    if (data == NULL)
    {
        data = malloc(10*sizeof(char));
        if (data == NULL)
        {
            return;
        }
    }

    strcpy(data, "Initialize");
    printLine(data);
    free(data);
}

#endif