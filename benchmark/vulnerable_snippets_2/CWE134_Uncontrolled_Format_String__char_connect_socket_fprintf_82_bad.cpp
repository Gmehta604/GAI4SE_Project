
#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE134_Uncontrolled_Format_String__char_connect_socket_fprintf_82.h"

namespace CWE134_Uncontrolled_Format_String__char_connect_socket_fprintf_82
{

void CWE134_Uncontrolled_Format_String__char_connect_socket_fprintf_82_bad::action(char * data)
{
    fprintf(stdout, data);
}

}
#endif 
