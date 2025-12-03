#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE15_External_Control_of_System_or_Configuration_Setting__w32_82.h"

#include <windows.h>

namespace CWE15_External_Control_of_System_or_Configuration_Setting__w32_82
{

void CWE15_External_Control_of_System_or_Configuration_Setting__w32_82_bad::action(char * data)
{
    // Validate input
    size_t len = strlen(data);
    if (len > 0 && len <= MAX_COMPUTERNAME_LENGTH)
    {
        // Sanitize input
        char* sanitizedData = new char[len + 1];
        memset(sanitizedData, 0, len + 1);
        for (size_t i = 0; i < len; i++)
        {
            if (isalnum(data[i]) || data[i] == '-' || data[i] == '_')
            {
                sanitizedData[i] = data[i];
            }
        }
        // Use sanitized input in system call
        if (!SetComputerNameA(sanitizedData))
        {
            printLine("Failure setting computer name");
            exit(1);
        }
        delete[] sanitizedData;
    }
    else
    {
        printLine("Invalid computer name");
        exit(1);
    }
}

}
#endif