#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE427_Uncontrolled_Search_Path_Element__char_connect_socket_81.h"

namespace CWE427_Uncontrolled_Search_Path_Element__char_connect_socket_81
{

void CWE427_Uncontrolled_Search_Path_Element__char_connect_socket_81_bad::action(char * data) const
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