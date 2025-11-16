
#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE256_Plaintext_Storage_of_Password__w32_char_81.h"

namespace CWE256_Plaintext_Storage_of_Password__w32_char_81
{

void CWE256_Plaintext_Storage_of_Password__w32_char_81_bad::action(char * data) const
{
    {
        HANDLE pHandle;
        char * username = "User";
        char * domain = "Domain";
        if (LogonUserA(
                    username,
                    domain,
                    data,
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