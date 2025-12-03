#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE400_Resource_Exhaustion__connect_socket_for_loop_82.h"

namespace CWE400_Resource_Exhaustion__connect_socket_for_loop_82
{

void CWE400_Resource_Exhaustion__connect_socket_for_loop_82_bad::action(int count)
{
    {
        size_t i = 0;
        for (i = 0; i < (size_t)count && i < MAX_LOOP; i++)
        {
            printLine("Hello");
        }
    }
}

}
#endif