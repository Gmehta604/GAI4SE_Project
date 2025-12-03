#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE665_Improper_Initialization__char_cat_81.h"

namespace CWE665_Improper_Initialization__char_cat_81
{

void CWE665_Improper_Initialization__char_cat_81_bad::action(char * data) const
{
    {
        char source[100];
        memset(source, 'C', 100-1); 
        source[100-1] = '\0'; 
        
        strncat(data, source, 100-1);
        printLine(data);
    }
}

}
#endif