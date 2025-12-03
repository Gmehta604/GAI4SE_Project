#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE369_Divide_by_Zero__float_connect_socket_81.h"

namespace CWE369_Divide_by_Zero__float_connect_socket_81
{

void CWE369_Divide_by_Zero__float_connect_socket_81_bad::action(float data) const
{
    {
        int result = (int)(100.0 / data);
        printIntLine(result);
    }
}

}
#endif 
