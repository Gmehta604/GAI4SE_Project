#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE134_Uncontrolled_Format_String__char_connect_socket_fprintf_81.h"

namespace CWE134_Uncontrolled_Format_String__char_connect_socket_fprintf_81
{

void CWE134_Uncontrolled_Format_String__char_connect_socket_fprintf_81_bad::action(const char * data) const
{
    fprintf(stdout, "%s", data);
}

}
#endif