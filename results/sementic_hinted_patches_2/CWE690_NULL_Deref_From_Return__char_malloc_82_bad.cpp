#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE690_NULL_Deref_From_Return__char_malloc_82.h"

namespace CWE690_NULL_Deref_From_Return__char_malloc_82
{

void CWE690_NULL_Deref_From_Return__char_malloc_82_bad::action(char * data)
{
    
    char * dataBuffer = (char *)malloc(100*sizeof(char));
    if (dataBuffer == NULL) {exit(-1);}
    strncpy(dataBuffer, "Initialize", 100-1);
    dataBuffer[100-1] = '\0';
    printLine(dataBuffer);
    free(dataBuffer);
}

}
#endif