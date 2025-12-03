
#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE319_Cleartext_Tx_Sensitive_Info__w32_char_connect_socket_82.h"

#include <windows.h>
#pragma comment(lib, "advapi32.lib")

#define HASH_INPUT "ABCDEFG123456" 

namespace CWE319_Cleartext_Tx_Sensitive_Info__w32_char_connect_socket_82
{

void CWE319_Cleartext_Tx_Sensitive_Info__w32_char_connect_socket_82_bad::action(char * password)
{
    {
        HANDLE pHandle;
        char * username = "User";
        char * domain = "Domain";
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
