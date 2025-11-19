#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE427_Uncontrolled_Search_Path_Element__char_connect_socket_81.h"

namespace CWE427_Uncontrolled_Search_Path_Element__char_connect_socket_81
{

void CWE427_Uncontrolled_Search_Path_Element__char_connect_socket_81_bad::action(char * data) const
{
    getenv(data);
}

}
#endif