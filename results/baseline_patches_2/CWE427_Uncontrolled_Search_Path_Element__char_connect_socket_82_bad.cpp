#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE427_Uncontrolled_Search_Path_Element__char_connect_socket_82.h"

namespace CWE427_Uncontrolled_Search_Path_Element__char_connect_socket_82
{

void CWE427_Uncontrolled_Search_Path_Element__char_connect_socket_82_bad::action(char * data)
{
    size_t dataLen = strlen(data);
    char * environment = GETENV(ENV_VARIABLE);
    /* If there is data in the environment variable */
    if (environment != NULL)
    {
        /* POTENTIAL FLAW: Read data from an environment variable */
        strncat(data+dataLen, environment, 100-dataLen-1);
    }
    PUTENV(data);
}

}
#endif