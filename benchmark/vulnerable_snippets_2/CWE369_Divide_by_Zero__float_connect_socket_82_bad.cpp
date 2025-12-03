
#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE369_Divide_by_Zero__float_connect_socket_82.h"

namespace CWE369_Divide_by_Zero__float_connect_socket_82
{

void CWE369_Divide_by_Zero__float_connect_socket_82_bad::action(float data)
{
    {
        int result = (int)(100.0 / data);
        printIntLine(result);
    }
}

}
#endif 
