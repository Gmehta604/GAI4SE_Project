#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE259_Hard_Coded_Password__w32_char_81.h"

#include <windows.h>
#pragma comment(lib, "advapi32.lib")

namespace CWE259_Hard_Coded_Password__w32_char_81
{

void CWE259_Hard_Coded_Password__w32_char_81_bad::action(char * password) const
{
    {
        HANDLE pHandle;
        char * username = "User";
        char * domain = "Domain";
        if (LogonUserA(
                    username,
                    domain,
                    NULL,
                    LOGON32_LOGON_NETWORK,
                    LOGON32_PROVIDER_DEFAULT,
                    &pHandle) != 0)
        {
            printLine("User logged in successfully.");
            CloseHandle(pHandle);
        }
        else
        {
            printLine("Unable to login.");
        }
    }
}

}
#endif