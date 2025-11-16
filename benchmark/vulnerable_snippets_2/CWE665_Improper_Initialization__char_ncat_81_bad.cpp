#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE665_Improper_Initialization__char_ncat_81.h"

namespace CWE665_Improper_Initialization__char_ncat_81
{

void CWE665_Improper_Initialization__char_ncat_81_bad::action(char * data) const
{
    {
        size_t sourceLen;
        char source[100];
        memset(source, 'C', 100-1); 
        source[100-1] = '\0'; 
        sourceLen = strlen(source);
        
        strncat(data, source, sourceLen);
        printLine(data);
    }
}

}
#endif 
