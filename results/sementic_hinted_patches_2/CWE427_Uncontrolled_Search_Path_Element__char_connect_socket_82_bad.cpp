#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE427_Uncontrolled_Search_Path_Element__char_connect_socket_82.h"

namespace CWE427_Uncontrolled_Search_Path_Element__char_connect_socket_82
{

void CWE427_Uncontrolled_Search_Path_Element__char_connect_socket_82_bad::action(char * data)
{
    char * env = strncpy(new char[strlen(data) + 1], data, strlen(data));
    PUTENV(env);
}

}
#endif