
#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE15_External_Control_of_System_or_Configuration_Setting__w32_82.h"

#include <windows.h>

namespace CWE15_External_Control_of_System_or_Configuration_Setting__w32_82
{

void CWE15_External_Control_of_System_or_Configuration_Setting__w32_82_bad::action(char * data)
{
    if (!SetComputerNameA(data))
    {
        printLine("Failure setting computer name");
        exit(1);
    }
}

}
#endif 