#ifndef OMITBAD

#include <stdlib.h>
#include <string.h>

void action(char * data) const
{
    if (data == NULL) {
        return;
    }

    strcpy(data, "Initialize");
    printLine(data);
    free(data);
}

#endif