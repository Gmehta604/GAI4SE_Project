#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE606_Unchecked_Loop_Condition__char_connect_socket_81.h"

namespace CWE606_Unchecked_Loop_Condition__char_connect_socket_81
{

void CWE606_Unchecked_Loop_Condition__char_connect_socket_81_bad::action(char * data) const
{
    {
        int i, n, intVariable;
        if (sscanf(data, "%d", &n) == 1)
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