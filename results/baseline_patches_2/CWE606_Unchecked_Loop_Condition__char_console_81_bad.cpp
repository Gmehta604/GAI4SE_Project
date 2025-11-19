#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE606_Unchecked_Loop_Condition__char_console_81.h"

namespace CWE606_Unchecked_Loop_Condition__char_console_81
{

void CWE606_Unchecked_Loop_Condition__char_console_81_bad::action(char * data) const
{
    {
        int i, n, intVariable;
        if (sscanf(data, "%d", &n) == 1 && n > 0 && n <= INT_MAX)
        {
            
            intVariable = 0;
            for (i = 0; i < n; i++)
            {
                
                intVariable++; 
            }
            printIntLine(intVariable);
        }
    }
}

}
#endif