#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE617_Reachable_Assertion__connect_socket_81.h"

namespace CWE617_Reachable_Assertion__connect_socket_81
{

void CWE617_Reachable_Assertion__connect_socket_81_bad::action(int data) const
{
    
    if (data <= ASSERT_VALUE)
    {
        throw std::invalid_argument("Invalid argument");
    }
}

}
#endif