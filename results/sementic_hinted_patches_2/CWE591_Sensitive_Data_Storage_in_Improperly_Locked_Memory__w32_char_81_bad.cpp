#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE591_Sensitive_Data_Storage_in_Improperly_Locked_Memory__w32_char_81.h"

#pragma comment(lib, "advapi32.lib")

namespace CWE591_Sensitive_Data_Storage_in_Improperly_Locked_Memory__w32_char_81
{

void CWE591_Sensitive_Data_Storage_in_Improperly_Locked_Memory__w32_char_81_bad::action(std::string password) const
{
    {
        HANDLE pHandle;
        std::string username = "User";
        std::string domain = "Domain";
        
        if (LogonUserA(
                    username,
                    domain,
                    password,
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