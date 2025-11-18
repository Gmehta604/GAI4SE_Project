To fix the divide-by-zero error in the given C++ code, you can add error checking to ensure that the divisor is not zero before performing the division operation. Here's an example of how you can modify the code to include error checking:
```c
#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE369_Divide_by_Zero__float_connect_socket_81.h"

namespace CWE369_Divide_by_Zero__float_connect_socket_81
{

void CWE369_Divide_by_Zero__float_connect_socket_81_bad::action(float data) const
{
    if (data != 0.0)
    {
        int result = (int)(100.0 / data);
        printIntLine(result);
    }
    else
    {
        printLine("Error: Divide by zero");
    }
}

}
#endif 
```
In this modified code, we check whether `data` is equal to zero before attempting to perform the division operation. If `data` is indeed zero, we print an error message instead of attempting the division.