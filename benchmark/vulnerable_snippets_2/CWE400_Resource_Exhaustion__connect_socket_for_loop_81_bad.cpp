#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE400_Resource_Exhaustion__connect_socket_for_loop_81.h"

namespace CWE400_Resource_Exhaustion__connect_socket_for_loop_81
{

void CWE400_Resource_Exhaustion__connect_socket_for_loop_81_bad::action(int count) const
{
    {
        size_t i = 0;
        for (i = 0; i < (size_t)count; i++)
        {
            printLine("Hello");
        }
    }
}

}
#endif 
